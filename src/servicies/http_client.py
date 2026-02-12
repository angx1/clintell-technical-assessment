import os
import json
from typing import Dict, Any
from dotenv import load_dotenv
import logging

load_dotenv()

class HttpClient:
    def __init__(self):
        self._token = os.getenv("RINGR_API_TOKEN")
        if not self._token:
            raise Exception("No se encontró token de autenticación")

    def post(self, url: str, body: Dict[str, Any], parsed_data: Dict[str, Any]) -> Dict[str, Any]:
        headers = {
            "Authorization": f"Bearer {self._token}",
            "Content-Type": "application/json",
            **parsed_data
        }

        logging.info(f"POST request: {url} \n{headers} ")
        
        try:
            # response = requests.post(url, headers=headers, json=body)
            # return response

            return {
                "status_code": 200,
                "message": "OK",
            }
        except Exception as e:
            raise Exception(f"Error al hacer la petición: {e}")

