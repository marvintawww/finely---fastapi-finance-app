from jose import jwt, JWTError
from datetime import datetime, timezone, timedelta
import secrets

from config import SECRET
from utils.exceptions import TokenCreationError, TokenBlaklistError, LogoutError, TokenTypeError

class JWTService:
    def __init__(self, query_repo, command_repo):
        self.__query_repo = query_repo
        self.__command_repo = command_repo
    
    async def create_access_token(self, id: int) -> str:
        """Создание Access Token

        Args:
            id (int): ID-пользователя

        Raises:
            TokenCreationError: Ошибка создания токена

        Returns:
            str: Access Token
        """
        
        try:
            payload = {
                'sub': str(id),
                'exp': datetime.now(timezone.utc) + timedelta(minutes=15),
                'jti': secrets.token_urlsafe(32),
                'type': 'access'
            }
            
            return jwt.encode(payload, SECRET, algorithm='HS256')
        except (JWTError, ValueError, TypeError):
            raise TokenCreationError('Ошибка при создании Access Token')   
        
    async def create_refresh_token(self, id: int) -> str:
        """Создание Refresh Token

        Args:
            id (int): ID-пользователя

        Raises:
            TokenCreationError: Ошибка при создании Refresh Token

        Returns:
            str: Refresh Token
        """
        
        try:
            payload = {
                'sub': str(id),
                'exp': datetime.now(timezone.utc) + timedelta(days=7),
                'jti': secrets.token_urlsafe(32),
                'type': 'refresh'
            }
            
            return jwt.encode(payload, SECRET, algorithm='HS256')
        except (JWTError, ValueError, TypeError):
            raise TokenCreationError('Ошибка при создании Refresh Token')   
            
    async def create_token_pair(self, id: int) -> dict:
        """Создание пары токенов

        Args:
            id (int): ID-пользователя

        Returns:
            dict: Пара токенов
        """
        
        return {
            'access_token': await self.create_access_token(id),
            'refresh_token': await self.create_refresh_token(id)
        } 
        
    async def refresh_tokens(self, token: str) -> dict:
        """Обновление пары токенов

        Args:
            token (str): Текущий Refresh-токен

        Raises:
            TokenBlaklistError: Токен в черном списке
            TokenCreationError: Ошибка создания токена

        Returns:
            dict: Пара токенов
        """
        
        try:
            payload = jwt.decode(token, SECRET, algorithms=['HS256'])
            jti = payload.get('jti') 
            
            token_is_blacklisted = await self.__query_repo.get_by_jti(jti) 
            if token_is_blacklisted:
                raise TokenBlaklistError('Токен в черном списке')
            
            await self.__command_repo.add_to_blacklist(jti) 
            user_id = int(payload.get('sub')) 
            return await self.create_token_pair(user_id) 
        except (JWTError, ValueError, TypeError):
            raise TokenCreationError('Ошибка при обновлении токенов')
            
    async def logout(self, token: str):
        """Выход из аккаунта

        Args:
            token (_type_): Refresh-токен

        Raises:
            LogoutError: Ошибка выхода
        """
        
        try: 
            payload = jwt.decode(token, SECRET, algorithms=['HS256'])
            
            token_type = payload.get('type')
            if not token_type == 'refresh':
                raise TokenTypeError('Неверный тип токена')
            
            jti = payload.get('jti')
            await self.__command_repo.add_to_blacklist(jti)
        except JWTError:
            raise LogoutError('Невалидный токен')