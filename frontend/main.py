import streamlit as st
from streamlit_chat import message as chat_m
import os
from dotenv import load_dotenv
from routers.initialization import initialize_session_state
from routers.intro import (
    set_page_configuration,
    display_author_info,
    display_main_title,
    display_description,
    display_sources_info,
)
from routers.common import (
    reset_conversation,
    display_messages,
    parse_response,
    on_select_change,
)

from routers.ibm_generative_sdk import handle_ibm_sdk
from routers.other_files import handle_other_files, upload_f
from utils.token_validation import inputAPI_token
from utils.retrieve_function import get_source
from utils.chat_history_api_client import get_chat_history, save_chat_history

load_dotenv()
ENDPOINT = os.getenv("ENDPOINT")

set_page_configuration()
display_author_info()
display_main_title()
display_description()
display_sources_info()


if "token_valid" not in st.session_state or not st.session_state["token_valid"]:
    st.session_state.token_valid = inputAPI_token(ENDPOINT, st.session_state)

if st.session_state.token_valid:
    # Source Selection
    options = ["IBM Generative SDK", "Other files"]

    selected_option = st.sidebar.selectbox(
        "Choose a source:", options, key="selectbox_key", on_change=on_select_change
    )

    st.session_state = initialize_session_state(selected_option, st.session_state)

    if selected_option == "Other files":
        with st.spinner("Loading..."):
            uploaded_file = st.sidebar.file_uploader(
                "Choose a file (PDF, CSV, TXT)", type=["pdf", "csv", "txt"]
            )
            if uploaded_file is not None:
                # reset_conversation(selected_option,st.session_state)
                st.session_state.text_data = upload_f(uploaded_file)
            if st.sidebar.button("Reset Conversation"):
                reset_conversation(selected_option, st.session_state)

            # Display previous messages
            display_messages(st.session_state)

            # Input field for new message
            if prompt := st.chat_input("Write input to chatbot"):
                st.session_state.full_response = handle_other_files(
                    prompt, st.session_state.text_data, ENDPOINT
                )
                st.session_state.parsed_message = parse_response(
                    st.session_state.full_response
                )
                try:
                    chat_m(
                        st.session_state.parsed_message,
                        is_user=False,
                        avatar_style="thumbs",
                        allow_html=True,
                    )
                    # Append the response to the session state
                    st.session_state.messages.append(
                        {
                            "id": "",
                            "role": "assistant",
                            "content": st.session_state.parsed_message,
                        }
                    )
                    save_chat_history(
                        str(st.session_state.session_id),
                        [[prompt, st.session_state.parsed_message]],
                        ENDPOINT,
                    )
                except:
                    chat_m(
                        st.session_state.full_response,
                        is_user=False,
                        avatar_style="thumbs",
                        allow_html=True,
                    )
                    # Append the response to the session state
                    st.session_state.messages.append(
                        {
                            "id": "",
                            "role": "assistant",
                            "content": st.session_state.full_response,
                        }
                    )
                    save_chat_history(
                        str(st.session_state.session_id),
                        [[prompt, st.session_state.full_response]],
                        ENDPOINT,
                    )

    if selected_option == "IBM Generative SDK":
        # Reset conversation button
        if st.sidebar.button("Reset Conversation"):
            reset_conversation(selected_option, st.session_state)

        # Display previous messages
        display_messages(st.session_state)

        if prompt := st.chat_input("Write input to chatbot"):
            st.session_state.full_response = handle_ibm_sdk(
                prompt, ENDPOINT, st.session_state
            )
            try:
                st.session_state.source = "\n\nSource: {}".format(
                    get_source(st.session_state.full_response, ENDPOINT)
                )
            except:
                st.session_state.source = None
            st.session_state.parsed_message = parse_response(
                st.session_state.full_response
            )

            try:
                chat_m(
                    st.session_state.parsed_message + st.session_state.source,
                    is_user=False,
                    avatar_style="thumbs",
                    allow_html=True,
                )
                st.session_state.messages.append(
                    {
                        "id": "",
                        "role": "assistant",
                        "content": st.session_state.parsed_message
                        + st.session_state.source,
                    }
                )
                save_chat_history(
                    str(st.session_state.session_id),
                    [[prompt, st.session_state.parsed_message]],
                    ENDPOINT,
                )
            except:
                chat_m(
                    st.session_state.full_response + st.session_state.source,
                    is_user=False,
                    avatar_style="thumbs",
                    allow_html=True,
                )

                # Append the response to the session state
                st.session_state.messages.append(
                    {
                        "id": "",
                        "role": "assistant",
                        "content": st.session_state.full_response
                        + st.session_state.source,
                    }
                )
                save_chat_history(
                    str(st.session_state.session_id),
                    [[prompt, st.session_state.full_response]],
                    ENDPOINT,
                )
