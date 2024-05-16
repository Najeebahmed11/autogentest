import gradio as gr
import requests
import json

API_URL = "http://127.0.0.1:8003/api"

def create_session(user_id, workflow_config):
    """Creates a new chat session for a user with a specified workflow configuration."""
    if not workflow_config:
        return None, "workflow_config is required"
    try:
        workflow_config_parsed = json.loads(workflow_config)
    except json.JSONDecodeError:
        return None, "Invalid workflow_config format"
    response = requests.post(f"{API_URL}/sessions", json={"user_id": user_id, "workflow_config": workflow_config_parsed})
    if response.ok:
        return response.json()['data']['session_id'], None
    else:
        return None, response.text

def send_message(user_id, message, session_id, root_msg_id, workflow_config):
    """Sends a message within a specific session."""
    message_data = {
        "message": {
            "user_id": user_id,
            "session_id": session_id,
            "text": message,
            "role": "user",
            "content": message,
            "root_msg_id": root_msg_id
        },
        "workflow": json.loads(workflow_config),  # Assuming workflow_config is a JSON string
        "connection_id": "xyz-456",
        "user_id": user_id
    }
    response = requests.post(f"{API_URL}/messages", json=message_data)
    if response.ok:
        return response.json()
    else:
        return response.text

def chat_interface(user_id, message, workflow_config, session_id=None, root_msg_id="0"):
    """Handles sending messages and managing chat session."""
    if session_id is None or session_id == "None":
        session_id, error = create_session(user_id, workflow_config)
        if not session_id:
            return "Failed to initiate session: " + error, session_id

    if message.strip():
        response = send_message(user_id, message, session_id, root_msg_id, workflow_config)
        return response, session_id
    else:
        return "Please type a message.", session_id

def wrap_chat_interface(user_id, message, workflow_config, session_id, root_msg_id):
    """Wrapper function to maintain session state across Gradio interface calls."""
    response, new_session_id = chat_interface(user_id, message, workflow_config, session_id, root_msg_id)
    return response, new_session_id

with gr.Blocks() as app:
    with gr.Row():
        user_id_input = gr.Textbox(label="User ID", placeholder="Enter your User ID")
        message_input = gr.Textbox(label="Your Message", placeholder="Type your message here")
        workflow_config_input = gr.Textbox(label="Workflow Config", placeholder="Enter workflow configuration")
        session_id_input = gr.Textbox(label="Session ID", placeholder="Enter session ID if you have one")
        root_msg_id_input = gr.Textbox(label="Root message ID", placeholder="Enter root message ID if you have one")
        send_button = gr.Button("Send")
        responses_output = gr.Textbox(label="Responses", lines=4)

    send_button.click(
        wrap_chat_interface,
        inputs=[user_id_input, message_input, workflow_config_input, session_id_input, root_msg_id_input],
        outputs=[responses_output, session_id_input]
    )

app.launch()
