from passlib.context import CryptContext

class PasswordHasher:
    
    def __init__(self):
        self.__pwd_context = CryptContext(
            schemes=['argon2'], 
            deprecated='auto'
        )
        
    def hash_pw(self, pw: str) -> str:
        """Хэширование пароля

        Args:
            pw (str): Чистый пароль

        Returns:
            str: Хэшированный пароль
        """
        
        return self.__pwd_context.hash(pw)
    
    def verify_pw(self, plain_pw: str, hash_pw: str) -> bool:
        """Проверка пароля

        Args:
            plain_pw (str): Чистый пароль
            hash_pw (str): Хэшированный пароль

        Returns:
            bool: True если пароли совпадают, False - если нет
        """
        
        return self.__pwd_context.verify(plain_pw, hash_pw)