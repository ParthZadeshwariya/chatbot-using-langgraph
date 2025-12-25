from langgraph.graph import StateGraph, START, END
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from typing import TypedDict, Annotated
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph.message import add_messages
import requests
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.tools import tool
from langchain_tavily import TavilySearch
from dotenv import load_dotenv
import sqlite3

load_dotenv()

class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

llm = ChatGoogleGenerativeAI(model='gemini-2.0-flash')


@tool
def search_tool(query: str) -> list:
    """
    performs searching using Tavily Search"
    """
    search_tool = TavilySearch(
        max_results=5,
        topic="general"
    )
    result = search_tool.invoke({"query": query})
    return result['results']

@tool
def calculator(first_number: float, second_number:float, operation: str) -> dict:
    """
    Performs basic arithmetic operations.
    Supported operations: add, subtract, multiply, divide.
    """
    try:
        if operation == "add":
            result = first_number + second_number
        elif operation == "subtract":
            result = first_number - second_number
        elif operation == "multiply":
            result = first_number * second_number
        elif operation == "divide":
            if second_number == 0:
                return {"error": "Division by zero is not allowed."}
            result = first_number / second_number
        else:
            return {"error": "Invalid operation. Please use add, subtract, multiply, or divide."}
        
        return {"first_num": first_number, "second_num": second_number,"operation": operation, "result": result}
    
    except Exception as e:
        return {"error": str(e)}
    
@tool
def get_stock_price(symbol: str)-> dict:
    """
    Fetches the current stock price for a given symbol using AlphaVantage API.
    """
    url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey=S8MJZ48W30JLU2XE'  
    response = requests.get(url)
    return response.json()


tools = [search_tool, calculator, get_stock_price]
llm_with_tools = llm.bind_tools(tools)

tool_node = ToolNode(tools)

def chat_node(state: ChatState):
    messages = state['messages']

    response = llm_with_tools.invoke(messages)

    return {'messages': [response]}


conn = sqlite3.connect('chatbot.db', check_same_thread=False)
checkpointer = SqliteSaver(conn=conn)
graph = StateGraph(ChatState)

graph.add_node('chat_node', chat_node)

graph = StateGraph(ChatState)

graph.add_node("chat_node", chat_node)
graph.add_node("tools", tool_node)

graph.add_edge(START, "chat_node")
graph.add_conditional_edges("chat_node", tools_condition)
graph.add_edge("tools", "chat_node")

chatbot = graph.compile(checkpointer=checkpointer)

def retrieve_all_threads():
    all_threads = set()
    for checkpoint in checkpointer.list(None):
        all_threads.add(checkpoint.config['configurable']['thread_id'])
    return list(all_threads)