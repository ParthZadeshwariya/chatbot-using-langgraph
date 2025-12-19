# LangGraph Chatbot with Streamlit UI

This project is a sophisticated chatbot application that combines the power of **LangGraph** for stateful conversation management and **Streamlit** for an interactive user interface. It utilizes **Google Gemini** models for generating responses and maintains persistent chat history using a **SQLite** database.

## Features

- **Interactive UI**: Clean and responsive chat interface built with Streamlit.
- **Stateful Conversations**: Leverages LangGraph to manage chat state and context.
- **Persistent History**: Automatically saves conversation threads to a local SQLite database (`chatbot.db`).
- **Multiple Threads**: Users can create new chat sessions and switch between existing conversation threads seamlessly.
- **AI Integration**: Powered by Google's `gemini-2.0-flash` model via `langchain-google-genai`.

## Prerequisites

Ensure you have Python installed. You will need the following packages:

- `langgraph`
- `langchain-google-genai`
- `streamlit`
- `python-dotenv`
- `langchain-core`

## Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd <repository_directory>
    ```

2.  **Install dependencies:**
    You can install the necessary packages using pip:
    ```bash
    pip install langgraph langchain-google-genai streamlit python-dotenv langchain-core
    ```

3.  **Environment Setup:**
    Create a `.env` file in the root directory and add your Google API key:
    ```env
    GOOGLE_API_KEY=your_google_api_key_here
    ```

## Usage

To start the application, run the Streamlit frontend script:

```bash
streamlit run frontend.py
```

The application will open in your default web browser.

## Project Structure

- **`frontend.py`**: Handles the Streamlit user interface, manages session state, and interacts with the backend to send/receive messages.
- **`langgraphBackend.py`**: Defines the LangGraph structure, initializes the Google Gemini LLM, and sets up the SQLite checkpointer for persistence.
- **`chatbot.db`**: SQLite database file created automatically to store chat history (checkpoints).
