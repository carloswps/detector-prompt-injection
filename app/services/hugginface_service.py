import os

import requests


class HugginfaceService:
    def __init__(self):
        if not os.getenv("HF_TOKEN"):
            raise ValueError("Environment variable HF_TOKEN not set.")

        self.api_url = "https://router.huggingface.co/hf-inference/models/protectai/deberta-v3-base-prompt-injection"
        self.headers = {"Authorization": f"Bearer {os.getenv('HF_TOKEN')}"}

    def query(self, text):
        payload = {"inputs": text}
        response = requests.post(self.api_url, headers=self.headers, json=payload)

        if response.status_code == 200:
            return response.json()
        else:
            return {"error": "Failed to query Hugging Face API"}

    def is_injection(self, text):
        results = self.query(text)

        print(f"Hugging Face API Response: {results}")

        if not results:
            print("Error querying Hugging Face API")
            return False

        return results
