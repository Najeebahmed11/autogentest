import gradio as gr
import requests

API_URL = "http://127.0.0.1:8081/api"

def fetch_data(endpoint, user_id='', session_id='', model_id='', agent_id='', workflow_id=''):
    url = f"{API_URL}/{endpoint}"
    params = {}
    if user_id:
        params["user_id"] = user_id
    if session_id:
        params["session_id"] = session_id
    if model_id:
        params["model_id"] = model_id
    if agent_id:
        params["agent_id"] = agent_id
    if workflow_id:
        params["workflow_id"] = workflow_id
    try:
        response = requests.get(url, params=params)
        data = response.json()
        if data["status"]:
            return "\n".join([str(item) for item in data["data"]])
        else:
            return f"Failed to fetch data: {data['message']}"
    except Exception as e:
        return f"An error occurred: {str(e)}"

with gr.Blocks() as app:
    with gr.Row():
        endpoint_dropdown = gr.Dropdown(choices=["messages", "sessions", "skills", "agents", "models", "workflows"], label="Select Endpoint")
        user_id_input = gr.Textbox(label="User ID")
        session_id_input = gr.Textbox(label="Session ID")
        model_id_input = gr.Textbox(label="Model ID")
        agent_id_input = gr.Textbox(label="Agent ID")
        workflow_id_input = gr.Textbox(label="Workflow ID")
        fetch_button = gr.Button("Fetch Data")
        output = gr.Textbox(label="Output", interactive=False)
        
    fetch_button.click(
        fetch_data,
        inputs=[endpoint_dropdown, user_id_input, session_id_input, model_id_input, agent_id_input, workflow_id_input],
        outputs=output
    )

app.launch()
