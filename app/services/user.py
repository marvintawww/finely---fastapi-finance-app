from schemas.user import UserCreate, UserCreateDB

from utils.exceptions import RegisterError, UserNotFoundError, PasswordVerifyError
from schemas.user import LoginData

class UserService:
    """Сервис пользователей"""
    
    def __init__(self, query_repo, command_repo, password_hasher):
        self.__query_repo = query_repo
        self.__command_repo = command_repo
        self.__password_hasher = password_hasher
        
    async def create_user(self, data: UserCreate):
        """Создание пользователя

        Args:
            data (UserCreate): Данные для создания пользователя

        Raises:
            RegisterError: Ошибка регистрации

        Returns:
            _type_: Пользователя
        """
        
        existing = await self.__query_repo.get_by_login(data.login)
        
        if existing:
            raise RegisterError('Пользователь с таким именем уже существует!')
        
        hashed = self.__password_hasher.hash_pw(data.password)
        hashed_data = UserCreateDB(
            login=data.login,
            hashed_password=hashed
        )
        
        new_user = await self.__command_repo.create(hashed_data)
        return new_user
    
    async def authenticate(self, data: LoginData):
        """Вход в аккаунт

        Args:
            data (LoginData): Данные для входа

        Raises:
            UserNotFoundError: Пользователь с таким именем не найден
            PasswordVerifyError: Пароли не совпадают

        Returns:
            _type_: Возвращает пользователя
        """
        
        user = await self.__query_repo.get_by_login(data.login)
        if user is None:
            raise UserNotFoundError('Пользователь не найден')
        
        if not self.__password_hasher.verify_pw(data.password, user.hashed_password):
            raise PasswordVerifyError('Пароль не совпадает')
        
        return user
    
    async def get_user_by_id(self, user_id: int):
        """Получить пользователя по ID

        Args:
            user_id (int): ID пользователя

        Raises:
            UserNotFoundError: Пользователь не найден

        Returns:
            _type_: Пользователь
        """
        
        user = await self.__query_repo.get_by_id(user_id)
        if user is None:
            raise UserNotFoundError('Пользователь не найден')
        return user