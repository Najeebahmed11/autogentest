import gradio as gr
import requests
import datetime
import json

API_URL = "http://127.0.0.1:8081/api"

def fetch_workflows(user_id):
    """Fetches workflows associated with a user ID from the backend."""
    response = requests.get(f"{API_URL}/workflows", params={"user_id": user_id})
    if response.ok:
        workflows_data = response.json()
        if workflows_data['status']:
            workflows = workflows_data['data']
            workflow_details = [
                f"ID: {workflow['id']} - Name: {workflow['name']}, Type: {workflow['type']}, "
                f"Description: {workflow['description']}, Summary Method: {workflow['summary_method']}, "
                f"Timestamp: {workflow['timestamp']}, Sender: {workflow['sender']}, Receiver: {workflow['receiver']}"
                for workflow in workflows
            ]
            return "\n".join(workflow_details)
        else:
            return "Failed to fetch workflows: " + workflows_data['message']
    return "Failed to fetch workflows: " + response.text

def add_or_update_workflow(user_id, workflow_id, name, type, description, summary_method, timestamp, sender, receiver):
    """Adds or updates a workflow associated with a user ID to the backend."""
    workflow_data = {
        "user_id": user_id,
        "workflow": {
            "id": workflow_id,
            "name": name,
            "type": type,
            "description": description,
            "summary_method": summary_method,
            "timestamp": timestamp,
            "sender": json.dumps(sender),
            "receiver": json.dumps(receiver)
        }
    }
    response = requests.post(f"{API_URL}/workflows", json=workflow_data)
    if response.ok:
        return "Workflow added or updated successfully!"
    return "Failed to add or update workflow: " + response.text

def delete_workflow(user_id, workflow_id):
    """Deletes a workflow based on its ID and user ID by first fetching its details."""
    fetch_url = f"{API_URL}/workflows"
    try:
        fetch_response = requests.get(fetch_url, params={"user_id": user_id, "workflow_id": workflow_id})
        fetch_data = fetch_response.json()
        if fetch_data["status"] and fetch_data["data"]:
            workflow_details = next((item for item in fetch_data["data"] if item['id'] == workflow_id), None)
            if not workflow_details:
                return "No workflow found with the provided ID."

            # Now call delete with full workflow details
            url = f"{API_URL}/workflows/delete"
            payload = {
                "user_id": user_id,
                "workflow": workflow_details
            }
            response = requests.delete(url, json=payload)
            if response.ok:
                result_data = response.json()
                if result_data.get("status"):
                    return "Workflow deleted successfully!"
                else:
                    return f"Failed to delete workflow: {result_data.get('message', 'No additional error information provided')}"
            else:
                return f"Failed to delete workflow: HTTP status {response.status_code} - {response.reason}"
        else:
            return "Failed to fetch workflow details for deletion."
    except requests.RequestException as e:
        return f"Request failed: {e}"
    except ValueError as e:
        return "Failed to decode the response from the server."

with gr.Blocks() as app:
    with gr.Tab("List Workflows"):
        user_id_input_list_workflows = gr.Textbox(label="Enter User ID")
        workflows_output = gr.TextArea(label="Workflows", lines=10)
        fetch_workflows_button = gr.Button("Fetch Workflows")
        fetch_workflows_button.click(fetch_workflows, inputs=user_id_input_list_workflows, outputs=workflows_output)

    with gr.Tab("Add or Update Workflow"):
        user_id_input_add = gr.Textbox(label="User ID")
        workflow_id_input = gr.Textbox(label="Workflow ID (leave empty to add new)")
        workflow_name_input = gr.Textbox(label="Workflow Name")
        workflow_type_input = gr.Textbox(label="Workflow Type")
        workflow_description = gr.TextArea(label="Workflow Description")
        workflow_summary_method_input = gr.Textbox(label="Summary Method")
        workflow_timestamp_input = gr.Textbox(label="Timestamp", value=str(datetime.datetime.now()))
        workflow_sender_input = gr.JSON(label="Sender")
        workflow_receiver_input = gr.JSON(label="Receiver")
        add_button = gr.Button("Add/Update Workflow")
        add_workflow_output = gr.Textbox()
        add_button.click(
            add_or_update_workflow,
            inputs=[
                user_id_input_add, workflow_id_input, workflow_name_input, workflow_type_input, 
                workflow_description, workflow_summary_method_input, workflow_timestamp_input, 
                workflow_sender_input, workflow_receiver_input
            ],
            outputs=add_workflow_output
        )

    with gr.Tab("Delete Workflow"):
        user_id_input_del = gr.Textbox(label="User ID")
        workflow_id_input_del = gr.Textbox(label="Workflow ID")
        delete_button = gr.Button("Delete Workflow")
        delete_workflow_output = gr.Textbox()
        delete_button.click(delete_workflow, inputs=[user_id_input_del, workflow_id_input_del], outputs=delete_workflow_output)

app.launch()
