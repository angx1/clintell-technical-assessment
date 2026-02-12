import pytest
from unittest.mock import Mock, patch
from src.agents.debt import DebtAgent
from src.models.mocks import ConversationModel, ParserModel
from datetime import date, timedelta



def test_debt_agent_registers_debt_with_valid_data():
    commitment_date = (date.today() + timedelta(days=10)).strftime('%Y-%m-%d')
    committed_amount = 150.50

    conversation = ConversationModel(["Pagaré {committed_amount} euros el {commitment_date}"])
    parser = ParserModel([{"commitment_date": commitment_date, "committed_amount": committed_amount}])
    http_client_mock = Mock()
    
    agent = DebtAgent(conversation, parser, http_client_mock)
    result = agent.handle_turn()
    
    assert result is not None
    assert result["commitment_date"] == commitment_date
    assert result["committed_amount"] == committed_amount
    http_client_mock.post.assert_called_once()


def test_debt_agent_skips_debt_with_no_data():
    conversation = ConversationModel(["Hola"])
    parser = ParserModel([{"commitment_date": None, "committed_amount": None}])
    http_client_mock = Mock()
    
    agent = DebtAgent(conversation, parser, http_client_mock)
    result = agent.handle_turn()
    
    assert result is None
    http_client_mock.post.assert_not_called()

def test_debt_agent_skips_action_with_invalid_date():
    commitment_date = (date.today() - timedelta(days=1)).strftime('%Y-%m-%d')
    committed_amount = 150.50

    conversation = ConversationModel(["Pagaré {committed_amount} euros el {commitment_date}"])
    parser = ParserModel([{"commitment_date": commitment_date, "committed_amount": committed_amount}])
    http_client_mock = Mock()
    
    agent = DebtAgent(conversation, parser, http_client_mock)
    
    with pytest.raises(Exception, match="Error al validar los datos"):
        agent.handle_turn()
    
    http_client_mock.post.assert_not_called()

def test_debt_agent_skips_action_with_invalid_amount():
    commitment_date = (date.today() + timedelta(days=10)).strftime('%Y-%m-%d')
    committed_amount = -150.50

    conversation = ConversationModel(["Pagaré {committed_amount} euros el {commitment_date}"])
    parser = ParserModel([{"commitment_date": commitment_date, "committed_amount": committed_amount}])
    http_client_mock = Mock()
    
    agent = DebtAgent(conversation, parser, http_client_mock)
    with pytest.raises(Exception, match="Error al validar los datos"):
        agent.handle_turn()
    
    http_client_mock.post.assert_not_called()


def test_debt_agent_prevents_duplicate_commitments():
    commitment_date = (date.today() + timedelta(days=10)).strftime('%Y-%m-%d')
    committed_amount = 150.50

    conversation = ConversationModel(["Pagaré {committed_amount} euros el {commitment_date}", "Pagaré {committed_amount} euros el {commitment_date}"])
    parser = ParserModel([{"commitment_date": commitment_date, "committed_amount": committed_amount}, {"commitment_date": commitment_date, "committed_amount": committed_amount}])
    http_client_mock = Mock()
    
    agent = DebtAgent(conversation, parser, http_client_mock)
    result1 = agent.handle_turn()
    assert http_client_mock.post.call_count == 1
    result2 = agent.handle_turn()
    assert http_client_mock.post.call_count == 1


def test_debt_agent_multiple_different_commitments():
    commitment_date1 = (date.today() + timedelta(days=10)).strftime('%Y-%m-%d')
    committed_amount1 = 150.50
    commitment_date2 = (date.today() + timedelta(days=20)).strftime('%Y-%m-%d')
    committed_amount2 = 200.50

    conversation = ConversationModel(["Pagaré {committed_amount1} euros el {commitment_date1}", "Pagaré {committed_amount2} euros el {commitment_date2}"])
    parser = ParserModel([{"commitment_date": commitment_date1, "committed_amount": committed_amount1}, {"commitment_date": commitment_date2, "committed_amount": committed_amount2}])
    http_client_mock = Mock()
    
    agent = DebtAgent(conversation, parser, http_client_mock)
    agent.handle_turn()
    agent.handle_turn()
    
    assert http_client_mock.post.call_count == 2
