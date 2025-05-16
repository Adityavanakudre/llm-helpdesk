import requests

HF_API_URL = "https://api-inference.huggingface.co/models/mistralai/Mixtral-8x7B-Instruct-v0.1"
HF_TOKEN = ""

headers = {
    "Authorization": f"Bearer {HF_TOKEN}"
}

def classify_and_draft(message):
    prompt = f"""
You are an IT helpdesk assistant.

Classify the user's issue into one of these categories:
["network-issue", "password-reset", "access-request", "hardware-issue", "software-bug", "general"]

Then generate a helpful response.

User Message:
\"\"\"
{message}
\"\"\"

Format your output exactly as:
Category: <category>
Response: <response>
"""

    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 150,
            "temperature": 0.7
        }
    }

    response = requests.post(HF_API_URL, headers=headers, json=payload)

    if response.status_code != 200:
        return {
            "category": "general",
            "draft": "Unable to process ticket at this time."
        }

    generated = response.json()[0]["generated_text"]

    # Parse output
    lines = generated.strip().splitlines()
    category = "general"
    draft = ""

    for line in lines:
        if line.lower().startswith("category:"):
            category = line.split(":", 1)[-1].strip()
        elif line.lower().startswith("response:"):
            draft = line.split(":", 1)[-1].strip()

    return {"category": category, "draft": draft}

