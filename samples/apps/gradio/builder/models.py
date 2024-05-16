import gradio as gr
import requests
import datetime
import json

API_URL = "http://127.0.0.1:8081/api"

def fetch_models(user_id):
    """Fetches models associated with a user ID from the backend and displays detailed information."""
    response = requests.get(f"{API_URL}/models", params={"user_id": user_id})
    if response.ok:
        models_data = response.json()
        if models_data['status']:
            models = models_data['data']
            model_details = [
                f"ID: {model['id']} - Model: {model['model']}, Description: {model['description']}, "
                f"Base URL: {model.get('base_url', 'N/A')}, API Key: {model.get('api_key', 'N/A')}, "
                f"API Type: {model.get('api_type', 'N/A')}, API Version: {model.get('api_version', 'N/A')}"
                for model in models
            ]
            return "\n".join(model_details)
        else:
            return "Failed to fetch models: " + models_data['message']
    return "Failed to fetch models: " + response.text

def add_or_update_model(user_id, model_id, model_name, description, base_url, api_key, api_type, api_version):
    """Adds or updates a model associated with a user ID to the backend."""
    model_data = {
        "user_id": user_id,
        "model": {
            "id": model_id,
            "model": model_name,
            "description": description,
            "base_url": base_url,
            "api_key": api_key,
            "api_type": api_type,
            "api_version": api_version
        }
    }
    response = requests.post(f"{API_URL}/models", json=model_data)
    if response.ok:
        return "Model added or updated successfully!"
    return "Failed to add or update model: " + response.text

def delete_model(user_id, model_id):
    """Deletes a model based on its ID and user ID by first fetching its details."""
    # Fetch the specific model details first
    fetch_url = f"{API_URL}/models"
    try:
        fetch_response = requests.get(fetch_url, params={"user_id": user_id, "model_id": model_id})
        fetch_data = fetch_response.json()
        print("data",fetch_data)
        if fetch_data["status"] and fetch_data["data"]:
            # Filter the correct model from the fetched data
            model_details = next((item for item in fetch_data["data"] if item['id'] == model_id), None)
            if not model_details:
                return "No model found with the provided ID."

            # Check if the model belongs to the user ID provided
            if model_details['user_id'] != user_id:
                return "Model does not belong to the user ID provided."

            # Now call delete with full model details
            url = f"{API_URL}/models/delete"
            payload = {
                "user_id": user_id,
                "model": model_details
            }
            response = requests.delete(url, json=payload)
            if response.ok:
                result_data = response.json()
                if result_data.get("status"):
                    return "Model deleted successfully!"
                else:
                    return f"Failed to delete model: {result_data.get('message', 'No additional error information provided')}"
            else:
                return f"Failed to delete model: HTTP status {response.status_code} - {response.reason}"
        else:
            return "Failed to fetch model details for deletion: " + fetch_data.get('message', 'No data available')
    except requests.RequestException as e:
        return f"Request failed: {e}"
    except ValueError as e:
        return "Failed to decode the response from the server."


with gr.Blocks() as app:
    with gr.Tab("List Models"):
        user_id_input_list = gr.Textbox(label="Enter User ID")
        models_output = gr.TextArea(label="Models", lines=10)
        fetch_button = gr.Button("Fetch Models")
        fetch_button.click(fetch_models, inputs=user_id_input_list, outputs=models_output)

    with gr.Tab("Add or Update Model"):
        user_id_input_add = gr.Textbox(label="User ID")
        model_id_input = gr.Textbox(label="Model ID (leave empty to add new)")
        model_name_input = gr.Textbox(label="Model Name")
        model_description = gr.TextArea(label="Model Description")
        base_url_input = gr.Textbox(label="Base URL")
        api_key_input = gr.Textbox(label="API Key")
        api_type_input = gr.Textbox(label="API Type (e.g., azure)")
        api_version_input = gr.Textbox(label="API Version (optional)")
        add_button = gr.Button("Add/Update Model")
        add_model_output = gr.Textbox()
        add_button.click(
            add_or_update_model,
            inputs=[user_id_input_add, model_id_input, model_name_input, model_description, base_url_input, api_key_input, api_type_input, api_version_input],
            outputs=add_model_output
        )

    with gr.Tab("Delete Model"):
        user_id_input_del = gr.Textbox(label="User ID")
        model_id_input_del = gr.Textbox(label="Model ID")
        delete_button = gr.Button("Delete Model")
        delete_model_output = gr.Textbox()
        delete_button.click(delete_model, inputs=[user_id_input_del, model_id_input_del], outputs=delete_model_output)

app.launch()