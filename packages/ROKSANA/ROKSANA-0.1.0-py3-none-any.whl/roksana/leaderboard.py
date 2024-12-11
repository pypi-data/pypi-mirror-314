import requests
from typing import Any

class LeaderboardClient:
    def __init__(self, api_url: str, api_key: str):
        self.api_url = api_url
        self.api_key = api_key

    def submit_result(self, user_id: str, result: Any):
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        payload = {
            'user_id': user_id,
            'result': result
        }
        response = requests.post(f"{self.api_url}/submit", json=payload, headers=headers)
        if response.status_code == 200:
            print("Submission successful!")
        else:
            print(f"Submission failed: {response.text}")

    def get_leaderboard(self):
        headers = {
            'Authorization': f'Bearer {self.api_key}',
        }
        response = requests.get(f"{self.api_url}/leaderboard", headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to fetch leaderboard: {response.text}")
