import requests
import json
import streamlit as st


def validate_token(token, model, end_point):
    """
    Validates the provided API token by sending a request to the specified endpoint.

    Args:
        token (str): The API token to be validated.
        model (str): The model associated with the API token.
        end_point (str): The endpoint URL for token validation.

    Returns:
        Response or str: The response object from the server if the request is successful, or an error message string in case of a RequestException.

    This function sends a POST request to the server to validate the given API token and model. It handles any request exceptions and returns the server's response or an error message.
    """
    url = "http://{}/update_api_key/".format(end_point)
    headers = {"accept": "application/json", "Content-Type": "application/json"}
    # data = json.dumps(token)
    data = {"api_key": token, "model": model}

    try:
        response = requests.post(url, headers=headers, params=data)
        return response
    except requests.RequestException as e:
        # Handle connection errors
        return f"An error occurred: {e}"


def inputAPI_token(ENDPOINT, session_state):
    """
    Handles the user input for the OpenAI API token and model selection in the Streamlit sidebar. Validates the token against a specified endpoint.

    Args:
        ENDPOINT (str): The endpoint URL for token validation.
        session_state (SessionState): The Streamlit session state object.

    Returns:
        bool: True if the token is validated successfully, False otherwise.

    This function allows the user to input their API token and select a model. It validates the token using `validate_token` function and updates the session state based on the validation result.
    """
    with st.spinner("Validating token..."):
        # User API Key Input
        user_api_key = st.sidebar.text_input(
            label="#### Insert your OpenAI API key:",
            placeholder="Paste your OpenAI API key, sk-",
            type="password",
        )
        # Model Selection
        model_option = st.sidebar.selectbox(
            label="Select a model:",
            options=["gpt-3.5-turbo-16k", "gpt-4-1106-preview", "gpt-4"],
        )

        # Confirmation Button
        confirm_button = st.sidebar.button("Confirm")

        if user_api_key and confirm_button:
            message = validate_token(user_api_key.strip(), model_option, ENDPOINT)
            try:
                if message.status_code == 200:
                    session_state["token_valid"] = True
                    st.sidebar.write(str(message.json()["message"]))
                    return session_state.token_valid
                else:
                    st.sidebar.write("Token is not valid. Please try another token.")
            except Exception as e:
                # Handle connection errors
                st.sidebar.write(
                    "Please try another token. Unexpected error: {}".format(e)
                )
