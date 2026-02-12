from typing import List, Dict, Any


class BaseModel:
    def __init__(self, data_secuence: List[Dict[str, Any]]):
        self._data_secuence = data_secuence
        self._current_turn = 0

    def get_current_turn(self) -> int:
        return self._current_turn

class ConversationModel(BaseModel):
    def answer_user(self) -> str:
        if self._current_turn < len(self._data_secuence):
            text = self._data_secuence[self._current_turn]
            self._current_turn += 1
            return text
        else:
            return "End of conversation."        

class ParserModel(BaseModel):
    def parse_data(self) -> Dict[str, Any]:
        if self._current_turn < len(self._data_secuence):
            data = self._data_secuence[self._current_turn]
            self._current_turn += 1
            return data
        else:
            return {}
