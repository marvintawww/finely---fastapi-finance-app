class DataValidationError(Exception):
    """Ошибка валидации"""
    pass

class TokenCreationError(Exception):
    """Ошибка валидации"""
    pass

class TokenBlaklistError(Exception):
    """Токен в черном списке"""
    pass

class TokenTypeError(Exception):
    """Токен в черном списке"""
    pass

class TokenDecodeError(Exception):
    """Ошибка декодинга токена"""
    pass

class CategoryTypeError(Exception):
    """Ошибка типа категории"""
    pass

class TransactionTypeError(Exception):
    """Ошибка типа транзакции"""
    pass

class RegisterError(Exception):
    """Ошибка регистрации"""
    pass

class LogoutError(Exception):
    """Ошибка логаута"""
    pass

class UserNotFoundError(Exception):
    """Пользователь не найден"""
    pass

class LoginError(Exception):
    """Ошибка логина"""
    pass

class PasswordVerifyError(Exception):
    """Ошибка верификации пароля"""
    pass

class CategoryExistingError(Exception):
    """Ошибка: Категория существует"""
    pass

class DeleteError(Exception):
    """Ошибка удаления"""
    pass

class CategoryNotFoundError(Exception):
    """Ошибка удаления"""
    pass

class NotFoundError(Exception):
    """Не найдено"""
    pass

class TypeMatchError(Exception):
    """Не найдено"""
    pass