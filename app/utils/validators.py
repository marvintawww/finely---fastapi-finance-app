from typing import Pattern
import re
 
from utils.exceptions import DataValidationError

def data_validator(data: str, patt: Pattern) -> bool:
    """Валидатор пароля

    Args:
        data (str): INPUT-DATA
        patt (Pattern): REGEX-паттерн

    Raises:
        DataValidationError: Ошибка валидации 

    Returns:
        bool: Вернет True если INPUT соответсвует требованиям паттерна, False - если нет
    """
    
    if re.match(patt, data):
        return data
    else:
        raise DataValidationError('Паттерн не соответствует всем требованиям')