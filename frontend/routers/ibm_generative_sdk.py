# ibm_generative_sdk.py
import requests
from routers.common import parse_prompt_code, set_history_prompt
from streamlit_chat import message as chat_m
import streamlit as st
from utils.chat_history_api_client import get_chat_history


def handle_ibm_sdk(prompt, end_point, session_state):
    """
    Handles the interaction with the IBM SDK for processing user prompts in a Streamlit app.

    Args:
        prompt (str): The user's input prompt.
        end_point (str): The endpoint URL of the IBM SDK service.
        session_state (SessionState): The current session state object of Streamlit.

    Returns:
        str: The full response from the IBM SDK service.

    This function appends the user's prompt to the session state, fetches chat history, and sends the prompt to the IBM SDK service. It then streams and displays the response.
    """
    st.session_state.messages.append({"role": "user", "content": prompt})
    chat_m(prompt, is_user=True, avatar_style="big-smile")

    try:
        history = get_chat_history(session_state.session_id, end_point)["chat_history"]
    except:
        history = []

    prompt_history = set_history_prompt(prompt, history, level=1)
    prompt_parsed = parse_prompt_code(prompt_history)

    with st.spinner("Generating..."):
        message_placeholder = st.empty()
        st.session_state.full_response = ""
        try:
            with requests.get(
                "http://{}/chat".format(end_point),
                stream=True,
                json={"text": prompt_parsed},
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
        except DuplicateWidgetID as e:
            message_placeholder.markdown("")
            return "You already asked this, rephrase your question!"
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
        finally:
            message_placeholder.markdown("")
            return st.session_state.full_response
