import pytest
from unittest.mock import Mock, patch
from src.agents.assistant import AssistantAgent
from src.models.mocks import ConversationModel, ParserModel


# I-07: Happy Path Testing
def test_assistant_agent_registers_request_with_valid_data():
    conversation = ConversationModel(["Tengo un problema con mi factura de enero"])
    parser = ParserModel([{"request": "Revisar factura de enero"}])
    http_client_mock = Mock()
    
    agent = AssistantAgent(conversation, parser, http_client_mock)
    result = agent.handle_turn()
    
    assert result is not None
    assert result["request"] == "Revisar factura de enero"
    http_client_mock.post.assert_called_once() 

# I-08: Behavioral Testing
def test_assistant_agent_skips_action_with_no_request():
    conversation = ConversationModel(["Hola"])
    parser = ParserModel([{"request": None}])
    http_client_mock = Mock()
    
    agent = AssistantAgent(conversation, parser, http_client_mock)
    result = agent.handle_turn()
    
    assert result is None
    http_client_mock.post.assert_not_called()

# I-09: Behavioral Testing
def test_assistant_agent_prevents_duplicate_requests():
    conversation = ConversationModel(["Tengo un problema con mi factura de enero", "Tengo un problema con mi factura de enero"])
    parser = ParserModel([{"request": "Revisar factura de enero"}, {"request": "Revisar factura de enero"}])
    http_client_mock = Mock()
    
    agent = AssistantAgent(conversation, parser, http_client_mock)
    result1 = agent.handle_turn()
    assert http_client_mock.post.call_count == 1
    result2 = agent.handle_turn()
    assert http_client_mock.post.call_count == 1

# I-10: Behavioral Testing
def test_assistant_agent_multiple_different_requests():
    conversation = ConversationModel(["Tengo un problema con mi factura de enero", "Necesito habalr con el proveedor de Y"])
    parser = ParserModel([{"request": "Revisar factura de enero"}, {"request": "Contactar proveedor de producto Y"}])
    http_client_mock = Mock()
    
    agent = AssistantAgent(conversation, parser, http_client_mock)
    agent.handle_turn()
    agent.handle_turn()
    
    assert http_client_mock.post.call_count == 2