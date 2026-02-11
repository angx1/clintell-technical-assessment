import os
import json
from typing import Dict, Any
from dotenv import load_dotenv

load_dotenv()

class HttpClient:
    def __init__(self):
        self._token = os.getenv("RINGR_API_KEY")
        if not self._token:
           # TODO: error logs

    def post(self, url: str, body: Dict[str, Any], parsed_data: Dict[str, Any]) -> Dict[str, Any]:
        headers = {
            "Authorization": f"Bearer {self._token}",
            "Content-Type": "application/json",
            **parsed_data
        }

        # TODO: simular logging de la petición
        
        try:
            # response = requests.post(url, headers=headers, json=body)
            # return response
            return {
                "status_code": 200,
                "message": "OK",
            }
        except requests.exceptions.RequestException as e:
            # TODO: error logs

