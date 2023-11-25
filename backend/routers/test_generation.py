import pytest
from dotenv import load_dotenv
from fastapi.testclient import TestClient
from config import settings
from main import app  # replace with your actual app import
from routers.generation import router, startup_event


client = TestClient(app)

load_dotenv(".env")


@pytest.fixture(autouse=True)
def run_before_tests():
    """
    A pytest fixture that runs before each test. It manually triggers the startup event
    to initialize necessary components for the test environment.
    """
    startup_event()


def test_health():
    """
    Tests the health check endpoint of the FastAPI application.

    Asserts:
    - The response status code is 200 (OK).
    - The response body matches the expected health check status.
    """
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "🤙"}


def test_get_current_model():
    """
    Tests the endpoint for retrieving the current model used by the application.

    Asserts:
    - The response status code is 200 (OK).
    - The response body contains the correct current model information.
    """
    response = client.get("/get_current_model/")
    assert response.status_code == 200
    assert response.json() == {
        "message": "Current model is {}".format(settings.LLM_NAME)
    }


def test_get_current_token():
    """
    Tests the endpoint for retrieving the current OpenAI API token used by the application.

    Asserts:
    - The response status code is 200 (OK).
    - The response body contains the correct current OpenAI API token.
    """
    response = client.get("/get_current_token/")
    assert response.status_code == 200
    assert response.json() == {"message": f"Current token is {settings.OPENAI_API_KEY}"}


def test_update_correct_token():
    """
    Tests the API key and model update endpoint with correct parameters.

    Asserts:
    - The response status code is 200 (OK).
    - The response body indicates successful update of the API key and model.
    """
    response = client.post(
        "/update_api_key/",
        params={
            "api_key": settings.OPENAI_API_KEY,
            "model": settings.LLM_NAME,
        },
        headers={"accept": "application/json", "Content-Type": "application/json"},
    )
    assert response.status_code == 200
    assert response.json() == {
        "message": "Your API Key and model are updated successfully."
    }


def test_update_wrong_token():
    """
    Tests the API key and model update endpoint with an incorrect API key.

    Asserts:
    - The response status code is 400 (Bad Request).
    - The response body contains an error message indicating a failure due to an incorrect API key.
    """
    response = client.post(
        "/update_api_key/",
        params={
            "api_key": " ",
            "model": settings.LLM_NAME,
        },
        headers={"accept": "application/json", "Content-Type": "application/json"},
    )
    print(str(response))
    assert response.status_code == 400
    assert (
        "Failed to update API key and model due to OpenAI API error:"
        in response.json()["detail"]
    )


def test_update_wrong_model():
    """
    Tests the API key and model update endpoint with an incorrect model name.

    Asserts:
    - The response status code is 400 (Bad Request).
    - The response body contains an error message indicating a failure due to an incorrect model name.
    """
    response = client.post(
        "/update_api_key/",
        params={
            "api_key": settings.OPENAI_API_KEY,
            "model": " ",
        },
        headers={"accept": "application/json", "Content-Type": "application/json"},
    )
    assert response.status_code == 400
    assert (
        "Failed to update API key and model due to OpenAI API error:"
        in response.json()["detail"]
    )


def test_chat_no_stream():
    """
    Tests the endpoint for handling conversational queries without streaming.

    Asserts:
    - The response status code is 200 (OK), indicating successful handling of the query.
    """
    response = client.get(
        "/chat_no_stream", params={"query": "Hello, answer with few words!"}
    )
    assert response.status_code == 200


def test_llm_chat_no_stream():
    """
    Tests the LLM conversational query handling endpoint without streaming, using provided context.

    Asserts:
    - The response status code is 200 (OK), indicating successful handling of the query with context.
    """
    response = client.get(
        "/llm_chat_no_stream",
        params={"query": "What is the first word ?", "context": "This is an example."},
    )
    assert response.status_code == 200


def test_get_document_source():
    """
    Tests the endpoint for retrieving document sources based on a given query.

    Asserts:
    - The response status code is 200 (OK), indicating successful retrieval of the document source.
    """
    response = client.get(
        "/get_document_source/", params={"query": "Where is maintainer SDK ?"}
    )
    assert response.status_code == 200
