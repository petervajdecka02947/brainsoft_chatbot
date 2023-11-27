# other_files.py
import streamlit as st
import pandas as pd
import requests
from streamlit_chat import message as chat_m
from routers.common import parse_prompt_code, set_history_prompt
import PyPDF2
from utils.chat_history_api_client import get_chat_history


def upload_f(uploaded_file):
    """
    Processes an uploaded file and returns its content as a string.

    Args:
        uploaded_file (UploadedFile): The file uploaded by the user.

    Returns:
        str: The content of the uploaded file as a string.

    This function supports CSV, PDF, and plain text files. It reads the file according to its type and returns its content.
    """
    file_type = uploaded_file.type
    if file_type == "text/csv":
        # Read CSV file
        df = pd.read_csv(uploaded_file)
        return df.to_string()
    elif file_type == "application/pdf":
        # Read PDF file
        reader = PyPDF2.PdfReader(uploaded_file)
        return "".join([page.extract_text() for page in reader.pages])
    elif file_type == "text/plain":
        # Read TXT file
        return uploaded_file.read().decode("utf-8")


def handle_other_files(end_point):
    """
    Handles the processing of user prompts and additional text data using an external service.

    Args:
        prompt (str): The user's input prompt.
        text_data (str): Additional text data to provide context for the prompt.
        end_point (str): The endpoint URL of the external service.

    Returns:
        str: The full response from the external service.

    This function sends the user's prompt and the additional text data to the specified endpoint. It streams and displays the response in the Streamlit app.
    """
    st.session_state.messages.append({"role": "user", "content": st.session_state.prompt})
    chat_m(st.session_state.prompt, is_user=True, avatar_style="big-smile")
    try:
        history = get_chat_history(st.session_state.session_id, end_point)[
            "chat_history"
        ]
    except:
        history = []
    st.session_state.prompt_history = set_history_prompt(st.session_state.prompt, history, level=1)
    st.session_state.prompt_parsed = parse_prompt_code(st.session_state.prompt_history)
    with st.spinner("Generating..."):
        message_placeholder = st.empty()
        st.session_state.full_response = ""
        try:
            with requests.get(
                "http://{}/llm_chat".format(end_point),
                stream=True,
                params={"query": st.session_state.prompt_parsed, "context": st.session_state.text_data},
                timeout=60,
            ) as r:
                r.raise_for_status()
                for line in r.iter_content(chunk_size=1024):
                    if line:
                        part = line.decode("utf-8")  # .replace("`","~")
                        st.session_state.full_response += part
                        try:
                            message_placeholder.markdown(
                                st.session_state.full_response + "▌"
                            )
                        except Exception as e:
                            print(f"Error updating message placeholder: {e}")
        except requests.exceptions.ChunkedEncodingError as e:
            print(f"Chunked Encoding Error occurred: {e}")
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
        finally:
            message_placeholder.markdown("")
            return st.session_state.full_response
