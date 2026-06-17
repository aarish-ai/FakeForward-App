import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

print("Testing OpenRouter...")
response = requests.post(
  url="https://openrouter.ai/api/v1/chat/completions",
  headers={
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    "Content-Type": "application/json",
  },
  data=json.dumps({
    "model": "nvidia/nemotron-4-340b-instruct:free",
    "messages": [
        {
          "role": "user",
          "content": "Test claim: The sky is blue. Score this 0-100."
        }
      ]
  }),
  timeout=20.0
)

print(response.status_code)
try:
    print(response.json())
except Exception as e:
    print(response.text)
