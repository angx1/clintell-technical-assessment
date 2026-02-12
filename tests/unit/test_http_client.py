import pytest
from unittest.mock import patch, MagicMock
from src.servicies.http_client import HttpClient
from dotenv import load_dotenv
import os

load_dotenv()

def test_http_client_with_valid_token():
    with patch('os.getenv', return_value=os.getenv('RINGR_API_TOKEN')):
        http_client = HttpClient()

    url = "https://api.ringr.test/v1/demo"
    body = {"message": "demo test"}
    parsed_data = {}
    
    result = http_client.post(url, body, parsed_data)
    
    assert result["status_code"] == 200
    assert result["message"] == "OK"


def test_http_client_with_no_token_raises_error():
    with patch('os.getenv', return_value=None):
        with pytest.raises(Exception, match='No se encontró token de autenticación'):
            http_client = HttpClient()

    

