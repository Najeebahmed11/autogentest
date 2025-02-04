{
  "status": true,
  "message": "Workflows retrieved successfully",
  "data": [
    {
      "name": "General Agent Workflow",
      "description": "This workflow is used for general purpose tasks.",
      "sender": {
        "type": "userproxy",
        "config": {
          "name": "userproxy",
          "llm_config": false,
          "human_input_mode": "NEVER",
          "max_consecutive_auto_reply": 10,
          "system_message": "You are a helpful assistant.",
          "is_termination_msg": null,
          "code_execution_config": {
            "work_dir": null,
            "use_docker": false
          },
          "default_auto_reply": "TERMINATE",
          "description": "A user proxy agent that executes code."
        },
        "id": "d0509530-3bc2-4eb8-8988-280d6c341951",
        "timestamp": "2024-05-02T19:31:52.038402",
        "user_id": "default",
        "skills": null
      },
      "receiver": {
        "type": "assistant",
        "config": {
          "name": "primary_assistant",
          "llm_config": {
            "config_list": [
              {
                "model": "gpt-4-1106-preview"
              }
            ],
            "temperature": 0.1,
            "cache_seed": null,
            "timeout": 600,
            "max_tokens": null,
            "extra_body": null
          },
          "human_input_mode": "NEVER",
          "max_consecutive_auto_reply": 15,
          "system_message": "You are a helpful AI assistant. Solve tasks using your coding and language skills. In the following cases, suggest python code (in a python coding block) or shell script (in a sh coding block) for the user to execute. 1. When you need to collect info, use the code to output the info you need, for example, browse or search the web, download/read a file, print the content of a webpage or a file, get the current date/time, check the operating system. After sufficient info is printed and the task is ready to be solved based on your language skill, you can solve the task by yourself. 2. When you need to perform some task with code, use the code to perform the task and output the result. Finish the task smartly. Solve the task step by step if you need to. If a plan is not provided, explain your plan first. Be clear which step uses code, and which step uses your language skill. When using code, you must indicate the script type in the code block. The user cannot provide any other feedback or perform any other action beyond executing the code you suggest. The user can't modify your code. So do not suggest incomplete code which requires users to modify. Don't use a code block if it's not intended to be executed by the user. If you want the user to save the code in a file before executing it, put # filename: <filename> inside the code block as the first line. Don't include multiple code blocks in one response. Do not ask users to copy and paste the result. Instead, use 'print' function for the output when relevant. Check the execution result returned by the user. If the result indicates there is an error, fix the error and output the code again. Suggest the full code instead of partial code or code changes. If the error can't be fixed or if the task is not solved even after the code is executed successfully, analyze the problem, revisit your assumption, collect additional info you need, and think of a different approach to try. When you find an answer, verify the answer carefully. Include verifiable evidence in your response if possible. Reply 'TERMINATE' in the end when everything is done.",
          "is_termination_msg": null,
          "code_execution_config": null,
          "default_auto_reply": "",
          "description": "Default assistant to generate plans and write code to solve tasks."
        },
        "id": "15855705-f8bd-4fe7-b228-ed8ab9162f17",
        "timestamp": "2024-05-02T19:31:52.038469",
        "user_id": "default",
        "skills": [
          {
            "title": "find_papers_arxiv",
            "content": "import os\nimport re\nimport json\nimport hashlib\n\n\ndef search_arxiv(query, max_results=10):\n    \"\"\"\n    Searches arXiv for the given query using the arXiv API, then returns the search results. This is a helper function. In most cases, callers will want to use 'find_relevant_papers( query, max_results )' instead.\n\n    Args:\n        query (str): The search query.\n        max_results (int, optional): The maximum number of search results to return. Defaults to 10.\n\n    Returns:\n        jresults (list): A list of dictionaries. Each dictionary contains fields such as 'title', 'authors', 'summary', and 'pdf_url'\n\n    Example:\n        >>> results = search_arxiv(\"attention is all you need\")\n        >>> print(results)\n    \"\"\"\n\n    import arxiv\n\n    key = hashlib.md5((\"search_arxiv(\" + str(max_results) + \")\" + query).encode(\"utf-8\")).hexdigest()\n    # Create the cache if it doesn't exist\n    cache_dir = \".cache\"\n    if not os.path.isdir(cache_dir):\n        os.mkdir(cache_dir)\n\n    fname = os.path.join(cache_dir, key + \".cache\")\n\n    # Cache hit\n    if os.path.isfile(fname):\n        fh = open(fname, \"r\", encoding=\"utf-8\")\n        data = json.loads(fh.read())\n        fh.close()\n        return data\n\n    # Normalize the query, removing operator keywords\n    query = re.sub(r\"[^\\s\\w]\", \" \", query.lower())\n    query = re.sub(r\"\\s(and|or|not)\\s\", \" \", \" \" + query + \" \")\n    query = re.sub(r\"[^\\s\\w]\", \" \", query.lower())\n    query = re.sub(r\"\\s+\", \" \", query).strip()\n\n    search = arxiv.Search(query=query, max_results=max_results, sort_by=arxiv.SortCriterion.Relevance)\n\n    jresults = list()\n    for result in search.results():\n        r = dict()\n        r[\"entry_id\"] = result.entry_id\n        r[\"updated\"] = str(result.updated)\n        r[\"published\"] = str(result.published)\n        r[\"title\"] = result.title\n        r[\"authors\"] = [str(a) for a in result.authors]\n        r[\"summary\"] = result.summary\n        r[\"comment\"] = result.comment\n        r[\"journal_ref\"] = result.journal_ref\n        r[\"doi\"] = result.doi\n        r[\"primary_category\"] = result.primary_category\n        r[\"categories\"] = result.categories\n        r[\"links\"] = [str(link) for link in result.links]\n        r[\"pdf_url\"] = result.pdf_url\n        jresults.append(r)\n\n    if len(jresults) > max_results:\n        jresults = jresults[0:max_results]\n\n    # Save to cache\n    fh = open(fname, \"w\")\n    fh.write(json.dumps(jresults))\n    fh.close()\n    return jresults\n",
            "file_name": null,
            "id": "cfd6a34d-82c1-41ac-831a-c58e69b31634",
            "description": "This skill finds relevant papers on arXiv given a query.",
            "timestamp": "2024-05-02T19:31:52.038450",
            "user_id": "default"
          },
          {
            "title": "generate_images",
            "content": "from typing import List\nimport uuid\nimport requests  # to perform HTTP requests\nfrom pathlib import Path\n\nfrom openai import OpenAI\n\n\ndef generate_and_save_images(query: str, image_size: str = \"1024x1024\") -> List[str]:\n    \"\"\"\n    Function to paint, draw or illustrate images based on the users query or request. Generates images from a given query using OpenAI's DALL-E model and saves them to disk.  Use the code below anytime there is a request to create an image.\n\n    :param query: A natural language description of the image to be generated.\n    :param image_size: The size of the image to be generated. (default is \"1024x1024\")\n    :return: A list of filenames for the saved images.\n    \"\"\"\n\n    client = OpenAI()  # Initialize the OpenAI client\n    response = client.images.generate(model=\"dall-e-3\", prompt=query, n=1, size=image_size)  # Generate images\n\n    # List to store the file names of saved images\n    saved_files = []\n\n    # Check if the response is successful\n    if response.data:\n        for image_data in response.data:\n            # Generate a random UUID as the file name\n            file_name = str(uuid.uuid4()) + \".png\"  # Assuming the image is a PNG\n            file_path = Path(file_name)\n\n            img_url = image_data.url\n            img_response = requests.get(img_url)\n            if img_response.status_code == 200:\n                # Write the binary content to a file\n                with open(file_path, \"wb\") as img_file:\n                    img_file.write(img_response.content)\n                    print(f\"Image saved to {file_path}\")\n                    saved_files.append(str(file_path))\n            else:\n                print(f\"Failed to download the image from {img_url}\")\n    else:\n        print(\"No image data found in the response!\")\n\n    # Return the list of saved files\n    return saved_files\n\n\n# Example usage of the function:\n# generate_and_save_images(\"A cute baby sea otter\")\n",
            "file_name": null,
            "id": "5f8e02db-fa43-4313-87d2-a7a0a4e9d1d6",
            "description": "This skill generates images from a given query using OpenAI's DALL-E model and saves them to disk.",
            "timestamp": "2024-05-02T19:31:52.038464",
            "user_id": "default"
          }
        ]
      },
      "type": "twoagents",
      "id": "f3d31040-de2a-4486-ae78-bad136ee5871",
      "user_id": "default",
      "timestamp": "2024-05-02T19:31:52.038728",
      "summary_method": "last"
    },
    {
      "name": "Travel Agent Group Chat Workflow",
      "description": "A group chat workflow",
      "sender": {
        "type": "userproxy",
        "config": {
          "name": "userproxy",
          "llm_config": false,
          "human_input_mode": "NEVER",
          "max_consecutive_auto_reply": 5,
          "system_message": "You are a helpful assistant.",
          "is_termination_msg": null,
          "code_execution_config": {
            "work_dir": null,
            "use_docker": false
          },
          "default_auto_reply": "",
          "description": null
        },
        "id": "e2df7265-aeb1-4a41-aead-04df2fb0e32a",
        "timestamp": "2024-05-02T19:31:52.037462",
        "user_id": "default",
        "skills": null
      },
      "receiver": {
        "type": "groupchat",
        "config": {
          "name": "group_chat_manager",
          "llm_config": {
            "config_list": [
              {
                "model": "gpt-4-1106-preview"
              }
            ],
            "temperature": 0.1,
            "cache_seed": 42,
            "timeout": 600,
            "max_tokens": null,
            "extra_body": null
          },
          "human_input_mode": "NEVER",
          "max_consecutive_auto_reply": 10,
          "system_message": "Group chat manager",
          "is_termination_msg": null,
          "code_execution_config": null,
          "default_auto_reply": "",
          "description": null
        },
        "groupchat_config": {
          "agents": [
            {
              "type": "assistant",
              "config": {
                "name": "travel_planner",
                "llm_config": {
                  "config_list": [
                    {
                      "model": "gpt-4-1106-preview"
                    }
                  ],
                  "temperature": 0.1,
                  "cache_seed": 42,
                  "timeout": 600,
                  "max_tokens": null,
                  "extra_body": null
                },
                "human_input_mode": "NEVER",
                "max_consecutive_auto_reply": 8,
                "system_message": "You are a helpful assistant that can suggest a travel plan for a user. You are the primary cordinator who will receive suggestions or advice from other agents (local_assistant, language_assistant). You must ensure that the finally plan integrates the suggestions from other agents or team members. YOUR FINAL RESPONSE MUST BE THE COMPLETE PLAN. When the plan is complete and all perspectives are integrated, you can respond with TERMINATE.",
                "is_termination_msg": null,
                "code_execution_config": null,
                "default_auto_reply": "",
                "description": null
              },
              "id": "38a1e140-dafb-4277-90aa-f7e70713b62b",
              "timestamp": "2024-05-02T19:31:52.037514",
              "user_id": "default",
              "skills": null
            },
            {
              "type": "assistant",
              "config": {
                "name": "local_assistant",
                "llm_config": {
                  "config_list": [
                    {
                      "model": "gpt-4-1106-preview"
                    }
                  ],
                  "temperature": 0.1,
                  "cache_seed": 42,
                  "timeout": 600,
                  "max_tokens": null,
                  "extra_body": null
                },
                "human_input_mode": "NEVER",
                "max_consecutive_auto_reply": 8,
                "system_message": "You are a helpful assistant that can review travel plans, providing critical feedback on how the trip can be enriched for enjoyment of the local culture. If the plan already includes local experiences, you can mention that the plan is satisfactory, with rationale.",
                "is_termination_msg": null,
                "code_execution_config": null,
                "default_auto_reply": "",
                "description": null
              },
              "id": "3a0da845-4d2b-437b-b78d-9e2c556501bf",
              "timestamp": "2024-05-02T19:31:52.037579",
              "user_id": "default",
              "skills": null
            },
            {
              "type": "assistant",
              "config": {
                "name": "language_assistant",
                "llm_config": {
                  "config_list": [
                    {
                      "model": "gpt-4-1106-preview"
                    }
                  ],
                  "temperature": 0.1,
                  "cache_seed": 42,
                  "timeout": 600,
                  "max_tokens": null,
                  "extra_body": null
                },
                "human_input_mode": "NEVER",
                "max_consecutive_auto_reply": 8,
                "system_message": "You are a helpful assistant that can review travel plans, providing feedback on important/critical tips about how best to address language or communication challenges for the given destination. If the plan already includes language tips, you can mention that the plan is satisfactory, with rationale.",
                "is_termination_msg": null,
                "code_execution_config": null,
                "default_auto_reply": "",
                "description": null
              },
              "id": "3348395e-ddb9-43dd-8863-1ebbe8636413",
              "timestamp": "2024-05-02T19:31:52.037589",
              "user_id": "default",
              "skills": null
            }
          ],
          "admin_name": "Admin",
          "messages": [],
          "max_round": 10,
          "speaker_selection_method": "auto",
          "allow_repeat_speaker": true
        },
        "id": "180a1a52-e09b-4005-91c9-9cada914652e",
        "timestamp": "2024-05-02T19:31:52.037610",
        "user_id": "default",
        "skills": null
      },
      "type": "groupchat",
      "id": "6b2360a2-9dba-4619-8b47-186c79c73e0d",
      "user_id": "default",
      "timestamp": "2024-05-02T19:31:52.037980",
      "summary_method": "last"
    }
  ]
}