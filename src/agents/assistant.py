from src.base import BaseAgent
from src.models.schemas import AssistantAgentSchema
from typing import Dict, Any, Optional
from dotenv import load_dotenv
import os


load_dotenv()

class AssistantAgent(BaseAgent):

    ENDPOINT = os.getenv("RINGR_ASSISTANCE_ENDPOINT")

    def _validate_normalize(self, raw_data: Dict[str, Any]) -> Optional[Any]:
        try:
            assistant_info = AssistantAgentSchema(**raw_data)
            if assistant_info.is_valid_request():
                return assistant_info.model_dump()

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