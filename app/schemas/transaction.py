from pydantic import BaseModel, ConfigDict, field_validator, Field
from typing import ClassVar, Pattern
from datetime import datetime

from utils.exceptions import TransactionTypeError
from app.utils.validators import data_validator
from utils.regex_patterns import DEFAULT_NAME_PATTERN

class TransactionCreate(BaseModel):
    """Схема валидации создания транзакции

    Args:
        BaseModel (_type_): Pydantic base класс

    Raises:
        TransactionTypeError: Ошибка типа транзакции/Неверный тип транзакции

    Returns:
        _type_: Валидная транзакция
    """
    
    name: str = Field(min_length=5, max_length=30)
    transaction_type: str
    category_id: int
    amount: float = Field(ge=0)
    
    TRANSACTION_NAME_PATTERN: ClassVar[Pattern] = DEFAULT_NAME_PATTERN
    
    @field_validator('name')
    @classmethod
    def name_checker(cls, name: str) -> str:
        return data_validator(name, cls.TRANSACTION_NAME_PATTERN)
    
    @field_validator('transaction_type')
    @classmethod
    def type_checker(cls, transaction_type: str) -> str:
        if transaction_type not in ('income', 'expense'):
            raise TransactionTypeError('Неверный тип транзакции')
        return transaction_type
    

class TransactionCreateDB(BaseModel):
    name: str
    transaction_type: str
    amount: float
    category_id: int
    user_id: int

class TransactionResponse(BaseModel):
    """Схема валидации ответа транзакции

    Args:
        BaseModel (_type_): Pydantic base класс
    """
    
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    name: str
    transaction_type: str
    amount: float
    category_id: int
    user_id: int
    created_at: datetime