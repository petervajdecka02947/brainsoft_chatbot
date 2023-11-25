from models import *
from utils.dependencies_generation import *
from utils.error_handler import *
from utils.callback_handler_agent import *
from utils.callback_handler_chain import *
from fastapi import APIRouter, HTTPException, Body
from config import settings
from dotenv import load_dotenv
from fastapi.responses import StreamingResponse
import logging


load_dotenv()

router = APIRouter()


def startup_event():
    """
    Event handler for application startup. Initializes the conversational agent, retriever, and LLM.
    This function sets up the conversational chain by calling `setup_conversational_chain` with the settings.

    Raises:
        HTTPException: An exception with the appropriate status code and message is raised if there is an error during initialization.
    """
    global agent
    global retriever
    global llm

    try:
        agent, retriever, llm = setup_conversational_chain(settings)

    except UpdateError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        msg = f"Unexpected error during agent initialization: {str(e)}"
        logging.error(msg)
        raise HTTPException(status_code=e.status_code, detail=msg)


router.add_event_handler("startup", startup_event)


@router.get("/health")
async def health():
    """
    Health check endpoint for the API.
    Returns the status of the API to indicate if it's running correctly.

    Returns:
        dict: A dictionary with the status of the API.
    """
    return {"status": "🤙"}


@router.post("/update_api_key/", status_code=200)
def update_api_key(api_key: str, model: str):
    """
    Updates the OpenAI API key and model. It reinitializes the agent, retriever, and LLM with the new settings.

    Args:
        api_key (str): The new API key for OpenAI.
        model (str): The model to be used with the new API key.

    Returns:
        dict: A message indicating successful update of the API Key and model.

    Raises:
        HTTPException: If there's a failure in updating the API Key and model.
    """
    global agent
    global retriever
    global llm

    try:
        settings = update_openai_api_key(api_key, model)
        agent, retriever, llm = setup_conversational_chain(settings)
        return {"message": f"Your API Key and model are updated successfully."}

    except UpdateError as e:
        raise HTTPException(
            status_code=e.status_code,
            detail=f"Failed to update API Key and model. Error: {e.message}",
        )
    except Exception as e:
        msg = f"Unexpected error during API key and model update: {str(e)}"
        logging.error(msg)
        raise HTTPException(status_code=e.status_code, detail=msg)


@router.get("/get_current_model/", status_code=200)
def get_current_model():
    """
    Retrieves the current model used by the LLM.

    Returns:
        dict: A message containing the current model name.

    Raises:
        HTTPException: If there's an error in retrieving the current model.
    """
    global llm

    try:
        return {"message": f"Current model is {str(llm.llm.model_name)}"}

    except UpdateError as e:
        raise HTTPException(
            status_code=e.status_code,
            detail=f"Failed to get model. Error: {e.message}",
        )
    except Exception as e:
        msg = f"Unexpected error during model getting: {str(e)}"
        logging.error(msg)
        raise HTTPException(status_code=500, detail=msg)


@router.get("/get_current_token/", status_code=200)
def get_current_token():
    """
    Retrieves the current OpenAI API token used by the LLM.

    Returns:
        dict: A message containing the current OpenAI API token.

    Raises:
        HTTPException: If there's an error in retrieving the current token.
    """
    global llm

    try:
        return {"message": f"Current token is {str(llm.llm.openai_api_key)}"}

    except UpdateError as e:
        raise HTTPException(
            status_code=e.status_code,
            detail=f"Failed to get token. Error: {e.message}",
        )
    except Exception as e:
        msg = f"Unexpected error during model getting: {str(e)}"
        logging.error(msg)
        raise HTTPException(status_code=500, detail=msg)


@router.get("/chat_no_stream", status_code=200)
async def chat_nostream(query: str):
    """
    Handles conversational queries without streaming.

    Args:
        query (str): The query string for the conversation.

    Returns:
        Response: The response from the conversational agent.

    Raises:
        HTTPException: If there's an error during the conversation generation.
    """
    global agent

    try:
        return await run_call_no_stream(agent=agent, query=query)

    except UpdateError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        msg = (
            f"Unexpected error during agent text generation without streaming: {str(e)}"
        )
        logging.error(msg)
        raise HTTPException(status_code=e.status_code, detail=msg)


@router.get("/llm_chat_no_stream", status_code=200)
async def llm_chat_nostream(query: str, context: str):
    """
    Handles LLM conversational queries without streaming, using the provided context.

    Args:
        query (str): The query string for the conversation.
        context (str): The context string to be used in conversation.

    Returns:
        Response: The response from the LLM.

    Raises:
        HTTPException: If there's an error during the conversation generation.
    """
    global llm

    try:
        return await llm_run_call_no_stream(llm=llm, query=query, context=context)

    except UpdateError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        msg = (
            f"Unexpected error during chain text generation without streaming: {str(e)}"
        )
        logging.error(msg)
        raise HTTPException(status_code=500, detail=msg)


@router.get("/chat", status_code=200)
async def chat(query: Query = Body(...), delay: float = 0.0):  # 0.1
    """
    Handles conversational queries with streaming.

    Args:
        query (Query): The query object containing the query string.
        delay (float, optional): Delay before sending the response. Defaults to 0.0.

    Returns:
        StreamingResponse: A streaming response for real-time conversation feedback.

    Raises:
        HTTPException: If there's an error during the conversation generation.
    """
    global agent

    try:
        stream_it = AsyncCallbackHandler(delay)
        gen = create_gen(agent, query, stream_it)
        return StreamingResponse(gen, media_type="text/event-stream")

    except UpdateError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        msg = f"Unexpected error during agent text generation: {str(e)}"
        logging.error(msg)
        raise HTTPException(status_code=500, detail=msg)


@router.get("/llm_chat", status_code=200)
async def chat(query: str, context: str, delay: float = 0.0):  # 0.1
    """
    Handles LLM conversational queries with streaming, using the provided context.

    Args:
        query (str): The query string for the conversation.
        context (str): The context string to be used in conversation.
        delay (float, optional): Delay before sending the response. Defaults to 0.0.

    Returns:
        StreamingResponse: A streaming response for real-time LLM conversation feedback.

    Raises:
        HTTPException: If there's an error during the conversation generation.
    """
    global llm

    try:
        stream_it = AsyncCallbackHandler_LLM(delay)
        gen = llm_create_gen(llm, query, context, stream_it)  # Query = Body(...)
        return StreamingResponse(gen, media_type="text/event-stream")

    except UpdateError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        msg = f"Unexpected error during agent text generation: {str(e)}"
        logging.error(msg)
        raise HTTPException(status_code=500, detail=msg)


@router.get("/get_document_source/", status_code=200)
async def get_document_source(query: str):
    """
    Retrieves the document source based on a given query.

    Args:
        query (str): The query string for retrieving the document source.

    Returns:
        Response: The retrieved document source.

    Raises:
        HTTPException: If there's an error during the document retrieval.
    """
    global retriever

    try:
        return await get_source(retriever, query)
    except Exception as e:
        msg = f"Unexpected error during document retrieval: {str(e)}"
        logging.error(msg)
        raise HTTPException(status_code=500, detail=msg)
