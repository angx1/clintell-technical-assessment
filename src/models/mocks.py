from typing import List, Dict, Any

class ConversationModel:
    def __init__(self, responses: List[str]):
        self._responses = responses
        self._current_turn = 0

    def answer_user(self) -> str:
        if self._current_turn < len(self._responses):
            text = self._responses[self._current_turn]
            self._current_turn += 1
            return text
        else:
            return "End of conversation."
        

class ParserModel:
    def __init__(self, data_secuence: List[Dict[str, Any]]):
        self._data_secuence = data_secuence
        self._current_turn = 0

    def parse_data(self) -> Dict[str, Any]:
        if self._current_turn < len(self._data_secuence):
            data = self._data_secuence[self._current_turn]
            self._current_turn += 1
            return data
        else:
            return {}
