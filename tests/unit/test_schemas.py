import pytest
from datetime import date, timedelta
from src.models.schemas import DebtAgentSchema, AssistantAgentSchema
import re

# DebtAgentSchema tests .--.-

def test_debt_agent_schema_valid_commitment():
    commitment_date = (date.today() + timedelta(days=1)).strftime('%Y-%m-%d')
    committed_amount = 100.00

    schema = DebtAgentSchema(commitment_date=commitment_date, committed_amount=committed_amount)

    assert schema.commitment_date == commitment_date
    assert schema.committed_amount == committed_amount
    assert schema.is_valid_commitment() is True


def test_debt_agent_schema_invalid_commitment():
    schema = DebtAgentSchema(commitment_date=None, committed_amount=None)

    assert schema.commitment_date is None
    assert schema.committed_amount is None
    assert schema.is_valid_commitment() is False


def test_debt_agent_schema_past_date_raises_error():
    with pytest.raises(Exception, match="La fecha debe ser posterior a hoy"):
        DebtAgentSchema(
            commitment_date=(date.today() - timedelta(days=1)).strftime('%Y-%m-%d'),
            committed_amount=100
        )

def test_debt_agent_schema_today_date_raises_error():
    with pytest.raises(Exception, match="La fecha debe ser posterior a hoy"):
        DebtAgentSchema(
            commitment_date=(date.today()).strftime('%Y-%m-%d'),
            committed_amount=100
        )


def test_debt_agent_schema_negative_amount_raises_error():
    with pytest.raises(Exception, match="El importe debe ser mayor a 0"):
        DebtAgentSchema(
            commitment_date=(date.today() + timedelta(days=1)).strftime('%Y-%m-%d'),
            committed_amount=-100
        )


def test_debt_agent_schema_0_amount_raises_error():
    with pytest.raises(Exception, match="El importe debe ser mayor a 0"):
        DebtAgentSchema(
            commitment_date=(date.today() + timedelta(days=1)).strftime('%Y-%m-%d'),
            committed_amount=0
        )


def test_debt_agent_schema_invalid_date_format_raises_error():
    with pytest.raises(Exception, match="Fecha inválida"):
        DebtAgentSchema(
            commitment_date="2026-13-01",
            committed_amount=100
        )


# AssistantAgentSchema tests .--.-

def test_assistant_agent_schema_valid_request():
    request = "Tengo un problema con una de mis factoras de enero"
    schema = AssistantAgentSchema(request=request)

    assert schema.request == request
    assert schema.is_valid_request() is True


def test_assistant_agent_schema_invalid_request():
    schema = AssistantAgentSchema(request=None)

    assert schema.request is None
    assert schema.is_valid_request() is False


def test_assistant_agent_schema_1000_characters_request_is_valid():
    schema = AssistantAgentSchema(request="a" * 1000)

    assert schema.is_valid_request() is True


def test_assistant_agent_schema_1001_characters_request_raises_error():
    with pytest.raises(Exception, match="La solicitud no puede tener más de 1000 caracteres"):
        AssistantAgentSchema(request="a" * 1001)



