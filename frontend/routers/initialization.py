from routers.common import reset_conversation
import bson


def initialize_session_state(selected_option: str, session_state: dict):
    """
    Initializes the session state variables for the Streamlit app.

    Args:
        selected_option (str): The selected option or category for the new session.
        session_state (dict): A dictionary representing the session state.

    Returns:
        dict: The updated session state with initialized values.

    This function ensures all necessary session state variables are initialized with default values or based on the selected option.
    """

    # Initialize session state for messages
    if "messages" not in session_state:
        reset_conversation(selected_option, session_state)

    # Initialize other session state variables with default values
    default_values = {
        "session_id": str(bson.ObjectId()),  #
        "current_message": "",
        "parsed_message": "",
        "parsed_message_strip": "",
        "full_response": "",
        "part": "",
        "prompt": "",
        "full_response": "",
        "parsed_message": "",
        "text_data": "",
        "chat_index": 0,
        "source": "",
    }

    for key, value in default_values.items():
        if key not in session_state:
            session_state[key] = value

    return session_state


# Usage in your main script
if __name__ == "__main__":
    selected_option = "Your Selected Option"  # Make sure to define or retrieve this value before calling the function
    initialize_session_state(selected_option)
