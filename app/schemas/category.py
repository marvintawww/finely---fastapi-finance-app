from pydantic import BaseModel, ConfigDict, field_validator, Field
from typing import ClassVar, Pattern

from app.utils.validators import data_validator
from utils.exceptions import CategoryTypeError
from utils.regex_patterns import DEFAULT_NAME_PATTERN

class CategoryCreate(BaseModel):
    """Схема создания категории

    Args:
        BaseModel (_type_): Родительский класс
    """
    
    name: str = Field(min_length=5, max_length=30)
    category_type: str
    
    CATEGORY_NAME_PATTERN: ClassVar[Pattern] = DEFAULT_NAME_PATTERN
    
    @field_validator('category_type')
    @classmethod
    def type_validator(cls, category_type: str):
        if category_type not in ('income', 'expense'):
            raise CategoryTypeError('Невалидный тип категории') 
        return category_type
    
    @field_validator('name')
    @classmethod
    def name_validator(cls, name: str):
        return data_validator(name, cls.CATEGORY_NAME_PATTERN)
    

class CategoryCreateDB(BaseModel):
    name: str
    category_type: str
    user_id: int    
    

class CategoryUpdate(BaseModel):
    name: str | None = None

    CATEGORY_NAME_PATTERN: ClassVar[Pattern] = DEFAULT_NAME_PATTERN

    @field_validator('name')
    @classmethod
    def name_validator(cls, name):
        if name is None:
            return name
        return data_validator(name, cls.CATEGORY_NAME_PATTERN)


class CategoryResponse(BaseModel):
    """Схема ответа категории

    Args:
        BaseModel (_type_): Pydantic base класс
    """
    
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    name: str
    category_type: str