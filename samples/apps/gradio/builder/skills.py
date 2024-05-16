import gradio as gr
import requests
import datetime
import logging
API_URL = "http://127.0.0.1:8081/api"

def fetch_skills(user_id):
    """Fetches skills associated with a user ID from the backend."""
    try:
        response = requests.get(f"{API_URL}/skills", params={"user_id": user_id})
        skills_data = response.json()
        if skills_data["status"]:
            skills = skills_data["data"]
            return "\n".join([f"ID: {skill['id']} - User Id: {skill['user_id']}, Description: {skill['description']}, File: {skill.get('file_name', 'N/A')}" for skill in skills])
        else:
            return "Failed to fetch skills: " + skills_data["message"]
    except Exception as e:
        return f"An error occurred: {str(e)}"

def add_or_update_skill(user_id, title, description, file_name):
    """Adds or updates a skill associated with a user ID to the backend."""
    skill_data = {
        "user_id": user_id,  # Note: moved user_id outside of the 'skill' dictionary
        "skill": {
            "timestamp": datetime.datetime.now().isoformat(),  # Ensure timestamp is properly formatted
            "content": description,
            "title": title,
            "file_name": file_name
        }
    }
    try:
        response = requests.post(f"{API_URL}/skills", json=skill_data)
        result_data = response.json()
        
        if result_data["status"]:
            return "Skill added or updated successfully!"
        else:
            return f"Failed to add or update skill: {result_data['message']}"
    except Exception as e:
        return f"An error occurred: {str(e)}"

def delete_skill(skill_id, user_id):
    """Deletes a skill based on its ID and associated user ID by first fetching its details."""
    # Fetch the skill details first
    fetch_url = f"{API_URL}/skills"
    try:
        fetch_response = requests.get(fetch_url, params={"user_id": user_id, "skill_id": skill_id})
        fetch_data = fetch_response.json()
        if fetch_data["status"] and fetch_data["data"]:
            skill_details = fetch_data["data"][0]  # Assuming the first skill is the one we want
            # Now call delete with full skill details
            url = f"{API_URL}/skills/delete"
            payload = {
                "user_id": user_id,
                "skill": {
                    "id": skill_details['id'],
                    "title": skill_details['title'],
                    "content": skill_details['content'],  # Assuming 'description' holds the content
                    "file_name": skill_details.get('file_name')  # Handle optional file_name
                }
            }
            response = requests.delete(url, json=payload)
            if response.ok:
                result_data = response.json()
                if result_data.get("status"):
                    return "Skill deleted successfully!"
                else:
                    return f"Failed to delete skill: {result_data.get('message', 'No additional error information provided')}"
            else:
                logging.error(f"Failed to delete skill: HTTP status {response.status_code} - {response.reason}")
                return f"Failed to delete skill: HTTP status {response.status_code} - {response.reason}"
        else:
            return "Failed to fetch skill details for deletion."
    except requests.RequestException as e:
        logging.error(f"Request failed: {e}")
        return "An error occurred during the request to the server."
    except ValueError as e:
        logging.error(f"Error decoding JSON: {e}")
        return "Failed to decode the response from the server."


with gr.Blocks() as app:
    with gr.Tab("List Skills"):
        with gr.Row():
            user_id_input_list = gr.Textbox(label="Enter User ID")
            skills_output = gr.Textbox(label="Skills", interactive=False, lines=10)
            fetch_button = gr.Button("Fetch Skills")
        fetch_button.click(
            fetch_skills,
            inputs=user_id_input_list,
            outputs=skills_output
        )

    with gr.Tab("Add or Update Skill"):
        with gr.Column():
            user_id_input_add = gr.Textbox(label="User ID")
            skill_title = gr.Textbox(label="Skill Title")
            skill_description = gr.TextArea(label="Skill Description", lines=3)
            skill_file_name = gr.Textbox(label="File Name")
            add_button = gr.Button("Add/Update Skill")
            add_skill_output = gr.Textbox(label="Result", interactive=False)
        add_button.click(
            add_or_update_skill,
            inputs=[user_id_input_add, skill_title, skill_description, skill_file_name],
            outputs=add_skill_output
        )

    with gr.Tab("Delete Skill"):
        with gr.Column():
            skill_id_input_del = gr.Textbox(label="ID")
            user_id_input_del = gr.Textbox(label="User ID for Deletion")
            delete_button = gr.Button("Delete Skill")
            delete_skill_output = gr.Textbox(label="Result", interactive=False)
        delete_button.click(
            delete_skill,
            inputs=[skill_id_input_del, user_id_input_del],
            outputs=delete_skill_output
        )

app.launch()
