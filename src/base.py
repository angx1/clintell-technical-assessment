from abc import ABC, abstractmethod
from typing import Dict, Any, Optional


class BaseAgent(ABC):

    def __init__(self, conversation_model: Any, parser_model: Any, http_client: Any):
        self.conversation_model = conversation_model
        self.parser_model = parser_model
        self.http_client = http_client

        self._action_history = set() 

    @abstractmethod
    def _validate_normalize(self, raw_data: Dict[str, Any]) -> Optional[Any]:
        pass

    @abstractmethod
    def _process_action(self, validated_data: Dict[str, Any], parsed_response: Dict[str, Any]) -> None:
        pass


    def handle_turn(self) -> str:
        response = self.conversation_model.answer_user()
        parsed_response = self.parser_model.parse_data()
        # parsed_response = self.parser_model.parse_data(response) ? dice que lógica interna de los modelos ya se ajusta osea que se opta por no pasar response

        validated_data = self._validate_normalize(parsed_response)
        if validated_data:
            action_key = frozenset(validated_data.items()) # clave de acción para evitar procesamiento de duplicados
            if action_key not in self._action_history:
                self._process_action(validated_data, parsed_response)
                self._action_history.add(action_key)

                
            # ElSE
                # TODO: error / warning logs
                
        return validated_data # self.conversation_model.answer_user()