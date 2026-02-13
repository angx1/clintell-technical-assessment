import pytest
from src.models.mocks import ConversationModel, ParserModel

# ConversationModel tests .--.-

# U-12: Happy Path Testing
def test_conversation_model_valid_responses():
    responses = ["Hola", "¿Cómo estás?", "¿Qué tal?"]
    conversation_model = ConversationModel(responses)
    assert conversation_model.answer_user() == "Hola"
    assert conversation_model.get_current_turn() == 1

    assert conversation_model.answer_user() == "¿Cómo estás?"
    assert conversation_model.get_current_turn() == 2

    assert conversation_model.answer_user() == "¿Qué tal?"
    assert conversation_model.get_current_turn() == 3

    assert conversation_model.answer_user() == "End of conversation."
    assert conversation_model.get_current_turn() == 3

# U-13: Edge Case Testing
def test_conversation_model_end_of_conversation():
    responses = ["Holaaaaaa"]
    conversation_model = ConversationModel(responses)
    assert conversation_model.answer_user() == "Holaaaaaa"
    assert conversation_model.get_current_turn() == 1

    assert conversation_model.answer_user() == "End of conversation."
    assert conversation_model.get_current_turn() == 1
    assert conversation_model.answer_user() == "End of conversation."
    assert conversation_model.get_current_turn() == 1
    assert conversation_model.answer_user() == "End of conversation."
    assert conversation_model.get_current_turn() == 1



# ParserModel tests .--.-

# U-14: Happy Path Testing
def test_parser_model_valid_data_sequence():
    data_sequence = [{"request": "revisión de factura de enero"}, {"request": "contactar proveedor de producto Y"}]
    parser_model = ParserModel(data_sequence)
    assert parser_model.parse_data() == {"request": "revisión de factura de enero"}
    assert parser_model.get_current_turn() == 1

    assert parser_model.parse_data() == {"request": "contactar proveedor de producto Y"}
    assert parser_model.get_current_turn() == 2

    assert parser_model.parse_data() == {}
    assert parser_model.get_current_turn() == 2

# U-15: Edge Case Testing
def test_parser_model_empty_data_sequence():
    data_sequence = []
    parser_model = ParserModel(data_sequence)

    assert parser_model.parse_data() == {}
    assert parser_model.get_current_turn() == 0

