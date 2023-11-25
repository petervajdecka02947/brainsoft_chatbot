import requests
from dotenv import load_dotenv
import os

load_dotenv()
BASE_URL = os.getenv("BASE_URL")

# CLI Functions corresponding to FastAPI endpoints


def health_check():
    """
    Performs a health check request to the FastAPI server.

    Returns:
        Response: The response object from the server indicating its health status.
    """
    return requests.get(f"{BASE_URL}/health")


def update_api_key(api_key):
    """
    Sends a request to update the API key in the FastAPI server.

    Args:
        api_key (str): The new API key to be updated in the server.

    Returns:
        Response: The response object from the server after attempting to update the API key.
    """
    return requests.post(f"{BASE_URL}/update_api_key/", json={"api_key": api_key})


def chat_nostream(query):
    """
    Sends a non-streaming chat query to the FastAPI server.

    Args:
        query (str): The chat query to be sent.

    Returns:
        Response: The response object from the server containing the chat response.
    """
    return requests.get(f"{BASE_URL}/chat_no_stream", params={"query": query})


def llm_chat_nostream(query, context):
    """
    Sends a non-streaming chat query with context to the FastAPI server's LLM endpoint.

    Args:
        query (str): The chat query to be sent.
        context (str): The context in which the query should be interpreted.

    Returns:
        Response: The response object from the server containing the LLM chat response.
    """
    return requests.get(
        f"{BASE_URL}/llm_chat_no_stream", params={"query": query, "context": context}
    )


def chat(query, delay):
    """
    Sends a streaming chat query to the FastAPI server with a specified delay.

    Args:
        query (str): The chat query to be sent.
        delay (float): The delay in seconds before sending the response.

    Returns:
        Response: The response object from the server containing the chat response.
    """
    return requests.get(f"{BASE_URL}/chat", params={"query": query, "delay": delay})


def llm_chat(query, context, delay):
    """
    Sends a streaming chat query with context to the FastAPI server's LLM endpoint with a specified delay.

    Args:
        query (str): The chat query to be sent.
        context (str): The context in which the query should be interpreted.
        delay (float): The delay in seconds before sending the response.

    Returns:
        Response: The response object from the server containing the LLM chat response.
    """
    return requests.get(
        f"{BASE_URL}/llm_chat",
        params={"query": query, "context": context, "delay": delay},
    )


def get_document_source(query):
    """
    Requests the source of a document based on a given query from the FastAPI server.

    Args:
        query (str): The query for which the document source is needed.

    Returns:
        Response: The response object from the server containing the source of the document.
    """
    return requests.get(f"{BASE_URL}/get_document_source/", params={"query": query})
