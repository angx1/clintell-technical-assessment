from datetime import datetime, date
from pydantic import BaseModel, Field, field_validator
from typing import Optional
import re


class DebtAgentSchema(BaseModel):
    commitment_date: Optional[str] = Field(None)
    committed_amount: Optional[float] = Field(None)

    @field_validator('commitment_date')
    @classmethod
    def validate_commitment_date(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return None
        try:
            v_parsed = datetime.strptime(v, '%Y-%m-%d').date() # format yyyy-mm-dd
        except ValueError:
            raise Exception('Fecha inválida (mes 1-12, día válido para el mes)')

        if v_parsed <= date.today(): # al ser commitment debe ser posterior a hoy
            raise Exception('La fecha debe ser posterior a hoy')
        return v

    @field_validator('committed_amount')
    @classmethod
    def validate_committed_amount(cls, v: Optional[float]) -> Optional[float]:
        if v is None:
            return None
        if v <= 0: # cantidad ha de ser mayor que 0
            raise Exception('El importe debe ser mayor a 0')
        return v

    def is_valid_commitment(self) -> bool:
        return self.commitment_date is not None and self.committed_amount is not None 



class AssistantAgentSchema(BaseModel):
    request: Optional[str] = Field(None)

    @field_validator('request')
    @classmethod
    def validate_request(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return None
        if len(v) > 1000: # max length of request para control de tokens
            raise Exception('La solicitud no puede tener más de 1000 caracteres')
        return v
    
    def is_valid_request(self) -> bool:
        return self.request is not None and len(self.request) <= 1000