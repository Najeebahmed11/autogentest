import gradio as gr
import requests
import datetime
import json

API_URL = "http://127.0.0.1:8081/api"

def fetch_agents(user_id):
    """Fetches agents associated with a user ID from the backend."""
    response = requests.get(f"{API_URL}/agents", params={"user_id": user_id})
    if response.ok:
        agents_data = response.json()
        if agents_data['status']:
            agents = agents_data['data']
            agent_details = [
                f"ID: {agent['id']} - Type: {agent['type']}, Config: {agent['config']}, "
                f"Skills: {agent['skills']}, Timestamp: {agent['timestamp']}"
                for agent in agents
            ]
            return "\n".join(agent_details)
        else:
            return "Failed to fetch agents: " + agents_data['message']
    return "Failed to fetch agents: " + response.text

def add_or_update_agent(user_id, agent_id, agent_type, config, skills, timestamp):
    """Adds or updates an agent associated with a user ID to the backend."""
    agent_data = {
        "user_id": user_id,
        "agent": {
            "id": agent_id,
            "type": agent_type,
            "config": json.dumps(config),
            "skills": json.dumps([skill.dict() for skill in skills]),
            "timestamp": timestamp
        }
    }
    response = requests.post(f"{API_URL}/agents", json=agent_data)
    if response.ok:
        return "Agent added or updated successfully!"
    return "Failed to add or update agent: " + response.text

def delete_agent(user_id, agent_id):
    """Deletes an agent based on its ID and user ID."""
    payload = {"user_id": user_id, "agent_id": agent_id}
    response = requests.delete(f"{API_URL}/agents/delete", json=payload)
    if response.ok:
        return "Agent deleted successfully!"
    return "Failed to delete agent: " + response.text

with gr.Blocks() as app:
    with gr.Tab("List Agents"):
        user_id_input_list_agents = gr.Textbox(label="Enter User ID")
        agents_output = gr.TextArea(label="Agents", lines=10)
        fetch_agents_button = gr.Button("Fetch Agents")
        fetch_agents_button.click(fetch_agents, inputs=user_id_input_list_agents, outputs=agents_output)

    with gr.Tab("Add or Update Agent"):
        user_id_input_add_agent = gr.Textbox(label="User ID")
        agent_id_input = gr.Textbox(label="Agent ID (leave empty to add new)")
        agent_type_input = gr.Textbox(label="Agent Type")
        agent_config_input = gr.TextArea(label="Agent Configuration (JSON)")
        agent_skills_input = gr.TextArea(label="Agent Skills (JSON)")
        agent_timestamp_input = gr.Textbox(label="Timestamp (ISO format)")
        add_agent_button = gr.Button("Add/Update Agent")
        add_agent_output = gr.Textbox()
        add_agent_button.click(
            add_or_update_agent,
            inputs=[user_id_input_add_agent, agent_id_input, agent_type_input, agent_config_input, agent_skills_input, agent_timestamp_input],
            outputs=add_agent_output
        )

    with gr.Tab("Delete Agent"):
        user_id_input_del_agent = gr.Textbox(label="User ID")
        agent_id_input_del = gr.Textbox(label="Agent ID")
        delete_agent_button = gr.Button("Delete Agent")
        delete_agent_output = gr.Textbox()
        delete_agent_button.click(delete_agent, inputs=[user_id_input_del_agent, agent_id_input_del], outputs=delete_agent_output)

app.launch()
