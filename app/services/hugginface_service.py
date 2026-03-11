import requests

from app import config


class HFService:
    def __init__(self):
        hf_token = config.HF_TOKEN
        if not hf_token:
            raise ValueError("Environment variable HF_TOKEN not set.")

        self.api_url = config.HF_API_URL
        self.headers = {"Authorization": f"Bearer {hf_token}"}

    def query(self, text):
        if not self.api_url:
            raise ValueError("Environment variable HF_API_URL not set.")

        payload = {"inputs": text}
        response = requests.post(self.api_url, headers=self.headers, json=payload)

        if response.status_code == 200:
            return response.json()
        else:
            return {"error": "Failed to query Hugging Face API"}

    def is_injection(self, text):
        results = self.query(text)

        if not results or isinstance(results, dict):
            print("Error querying Hugging Face API")
            return False

        candidates = results[0] if isinstance(results[0], list) else results

        for item in candidates:
            if item.get("label", "").upper() == "INJECTION":
                return item.get("score", 0) > 0.5

        return False
