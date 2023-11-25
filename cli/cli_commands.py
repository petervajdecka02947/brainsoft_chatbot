from api_client import (
    health_check,
    update_api_key,
    chat_nostream,
    llm_chat_nostream,
    chat,
    llm_chat,
    get_document_source,
)
from utils import format_response, handle_error


def setup_cli(parser):
    """
    Configures the command line interface (CLI) by setting up parsers for different commands.

    Args:
        parser (ArgumentParser): The argument parser for the CLI.

    This function adds subparsers for various commands like health check, API key update, chat operations, and more.
    Each subparser is configured with necessary arguments and default functions to execute for each command.
    """

    subparsers = parser.add_subparsers()

    # Health Check
    health_parser = subparsers.add_parser("health", help="Check API health")
    health_parser.set_defaults(func=health_command)

    # Update API Key
    update_key_parser = subparsers.add_parser("update_key", help="Update API key")
    update_key_parser.add_argument("api_key", type=str, help="API key")
    update_key_parser.set_defaults(func=update_key_command)

    # Chat No Stream
    chat_nostream_parser = subparsers.add_parser(
        "chat_nostream", help="Chat without streaming"
    )
    chat_nostream_parser.add_argument("query", type=str, help="Chat query")
    chat_nostream_parser.set_defaults(func=chat_nostream_command)

    # LLM Chat No Stream
    llm_chat_nostream_parser = subparsers.add_parser(
        "llm_chat_nostream", help="LLM Chat without streaming"
    )
    llm_chat_nostream_parser.add_argument("query", type=str, help="Chat query")
    llm_chat_nostream_parser.add_argument("context", type=str, help="Chat context")
    llm_chat_nostream_parser.set_defaults(func=llm_chat_nostream_command)

    # Chat with Stream
    chat_parser = subparsers.add_parser("chat", help="Chat with streaming")
    chat_parser.add_argument("query", type=str, help="Chat query")
    chat_parser.add_argument(
        "--delay", type=float, default=0.0, help="Delay for streaming"
    )
    chat_parser.set_defaults(func=chat_command)

    # LLM Chat with Stream
    llm_chat_parser = subparsers.add_parser("llm_chat", help="LLM Chat with streaming")
    llm_chat_parser.add_argument("query", type=str, help="Chat query")
    llm_chat_parser.add_argument("context", type=str, help="Chat context")
    llm_chat_parser.add_argument(
        "--delay", type=float, default=0.0, help="Delay for streaming"
    )
    llm_chat_parser.set_defaults(func=llm_chat_command)

    # Get Document Source
    get_document_source_parser = subparsers.add_parser(
        "get_document_source", help="Get document source"
    )
    get_document_source_parser.add_argument("query", type=str, help="Document query")
    get_document_source_parser.set_defaults(func=get_document_source_command)


def health_command(args):
    """
    Executes the health check command.

    Args:
        args: The command-line arguments provided for the health check command.

    This function calls the health check API and formats the response for display.
    It handles any exceptions that occur during the process.
    """
    try:
        response = health_check()
        format_response(response)
    except Exception as e:
        handle_error(e)


def update_key_command(args):
    """
    Executes the command to update the API key.

    Args:
        args: The command-line arguments provided for the update key command.

    This function calls the API to update the API key with the provided key and formats the response for display.
    It handles any exceptions that occur during the process.
    """
    try:
        response = update_api_key(args.api_key)
        format_response(response)
    except Exception as e:
        handle_error(e)


def chat_nostream_command(args):
    """
    Executes the command for non-streaming chat.

    Args:
        args: The command-line arguments provided for the chat non-streaming command.

    This function sends a non-streaming chat query to the server and formats the response for display.
    It handles any exceptions that occur during the process.
    """
    try:
        response = chat_nostream(args.query)
        format_response(response)
    except Exception as e:
        handle_error(e)


def llm_chat_nostream_command(args):
    """
    Executes the command for non-streaming LLM chat with context.

    Args:
        args: The command-line arguments provided for the LLM chat non-streaming command.

    This function sends a non-streaming LLM chat query with context to the server and formats the response for display.
    It handles any exceptions that occur during the process.
    """
    try:
        response = llm_chat_nostream(args.query, args.context)
        format_response(response)
    except Exception as e:
        handle_error(e)


def chat_command(args):
    """
    Executes the command for streaming chat.

    Args:
        args: The command-line arguments provided for the chat streaming command.

    This function sends a streaming chat query to the server and formats the response for display.
    It handles any exceptions that occur during the process.
    """
    try:
        response = chat(args.query, args.delay)
        format_response(response)
    except Exception as e:
        handle_error(e)


def llm_chat_command(args):
    """
    Executes the command for streaming LLM chat with context.

    Args:
        args: The command-line arguments provided for the LLM chat streaming command.

    This function sends a streaming LLM chat query with context to the server and formats the response for display.
    It handles any exceptions that occur during the process.
    """
    try:
        response = llm_chat(args.query, args.context, args.delay)
        format_response(response)
    except Exception as e:
        handle_error(e)


def get_document_source_command(args):
    """
    Executes the command to get the source of a document based on a query.

    Args:
        args: The command-line arguments provided for the get document source command.

    This function sends a query to the server to get the source of a document and formats the response for display.
    It handles any exceptions that occur during the process.
    """
    try:
        response = get_document_source(args.query)
        format_response(response)
    except Exception as e:
        handle_error(e)
