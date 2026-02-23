from pydantic import BaseModel, field_validator, ConfigDict, Field
from typing import ClassVar, Pattern

from app.utils.validators import data_validator
from utils.regex_patterns import PASS_PATTERN, LOGIN_PATTERN


class UserCreate(BaseModel):
    """Схема валидации данных для создания пользователя

    Args:
        BaseModel (_type_): Базовый класс Pydantic

    Returns:
        _type_: ? надо написать что возвращает ?
    """
    
    login: str = Field(min_length=5, max_length=30)
    password: str
    
    PW_PATTERN: ClassVar[Pattern] = PASS_PATTERN
    LN_PATTERN: ClassVar[Pattern] = LOGIN_PATTERN
    
    @field_validator('login')
    @classmethod
    def login_checker(cls, ln: str):
        return data_validator(ln, cls.LN_PATTERN)
    
    @field_validator('password')
    @classmethod
    def pass_checker(cls, pw: str):
        return data_validator(pw, cls.PW_PATTERN)
    

class UserCreateDB(BaseModel):
    
    login: str
    hashed_password: str
    

class UserResponse(BaseModel):
    """Схема отправки данных пользователю в качестве ответа"""
    
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    login: str
    

class LoginData(BaseModel):
    
    login: str
    password: str