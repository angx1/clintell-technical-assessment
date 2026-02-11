from src.base import BaseAgent
from src.models.schemas import DebtAgentSchema
from typing import Dict, Any, Optional
from dotenv import load_dotenv
import os


load_dotenv()

class DebtAgent(BaseAgent):

    ENDPOINT = os.getenv("RINGR_DEBT_ENDPOINT")

    def _validate_normalize(self, raw_data: Dict[str, Any]) -> Optional[Any]:
        try:
            debt_info = DebtAgentSchema(**raw_data)
            if debt_info.is_valid_commitment():
                return debt_info.model_dump()

            return None
        except Exception as e:
            raise Exception(f"Error al validar los datos: {e}")

    def _process_action(self, validated_data: Dict[str, Any], parsed_response: Dict[str, Any]) -> None:
        try:
            self.http_client.post(
                url=self.ENDPOINT,
                body=validated_data,
                parsed_data=parsed_response
            )
        except Exception as e:
            raise Exception(f"Error al hacer la petición: {e}")