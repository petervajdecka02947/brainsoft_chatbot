import requests
from dotenv import load_dotenv
import os
from typing import List

# Define the path to the .env file
env_path = os.path.join(os.path.dirname(__file__), "..", ".env")

# Load the .env file variables
load_dotenv(dotenv_path=env_path)

BASE_URL = os.getenv("BASE_URL")


def update_api_key(api_key: str):
    """
    Updates the OpenAI API key used by the chat service.

    Parameters:
    api_key (str): The new API key for OpenAI.

    Returns:
    dict: The response from the server.
    """
    url = f"{BASE_URL}/update_api_key/"
    response = requests.post(url, json={"api_key": api_key})
    response.raise_for_status()
    return response.json()


def chat(question: str, chat_history: List[List[str]]):
    """
    Sends a chat request to the server and receives a response.

    Parameters:
    question (str): The question to ask the chatbot.
    chat_history (List[List[str]]): The current chat history.

    Returns:
    dict: The chat response from the server.
    """
    url = f"{BASE_URL}/chat/"
    data = {"question": question, "chat_history": chat_history}
    response = requests.post(url, json=data)
    response.raise_for_status()
    return response.json()
