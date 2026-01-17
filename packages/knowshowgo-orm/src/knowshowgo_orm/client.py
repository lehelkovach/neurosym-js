from typing import Optional

import requests


class KnowShowGoClient:
    def __init__(self, base_url: str = "http://localhost:8000") -> None:
        self.base_url = base_url.rstrip("/")

    def process_instruction(self, text: str) -> dict:
        resp = requests.post(f"{self.base_url}/instructions", json={"text": text}, timeout=10)
        resp.raise_for_status()
        return resp.json()
