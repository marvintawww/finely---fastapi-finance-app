from fastapi import APIRouter, HTTPException, status, Depends
from jose import JWTError, ExpiredSignatureError

from schemas.user import UserCreate, LoginData, UserResponse
from schemas.token import TokenResponse, RefreshTokenRequest
from dependencies.user import get_user_service
from dependencies.jwt import get_jwt_service
from dependencies.auth import get_current_user
from services.user import UserService
from services.jwt import JWTService
from utils.exceptions import (
TokenCreationError, 
RegisterError, 
UserNotFoundError, 
PasswordVerifyError, 
TokenTypeError,
LogoutError,
TokenBlaklistError
)


router = APIRouter(prefix='/api/v1')


@router.post(
    '/register',
    response_model=TokenResponse,
    status_code=status.HTTP_201_CREATED,
    summary='Регистрация нового пользователя'
)
async def register(
    data: UserCreate, 
    user_service: UserService = Depends(get_user_service),
    jwt_service: JWTService = Depends(get_jwt_service)
) -> dict:
    """Endpoint регистрации нового пользователя

    Args:
        data (UserCreate): Данные с клиента
        user_service (UserService, optional): Инжект user сервиса. Defaults to Depends(get_user_service).
        jwt_service (JWTService, optional): Инжект jwt сервиса. Defaults to Depends(get_jwt_service).

    Raises:
        HTTPException: HTTP-ошибка

    Returns:
        dict: Пару токенов
    """
    try:
        user = await user_service.create_user(data)
        tokens = await jwt_service.create_token_pair(user.id)
        return tokens
    except TokenCreationError: 
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Ошибка при создании токенов'
        )
    except RegisterError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Пользователь с таким именем уже существует'
        )


@router.post(
    '/login',
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
    summary='Вход в аккаунт'
)
async def login(
    data: LoginData,
    user_service: UserService = Depends(get_user_service),
    jwt_service: JWTService = Depends(get_jwt_service) 
) -> dict:
    """Вход пользователя в аккаунт

    Args:
        data (LoginData): Данные для входа
        user_service (UserService, optional): Инжект user сервиса. Defaults to Depends(get_user_service).
        jwt_service (JWTService, optional): Инжект jwt сервиса. Defaults to Depends(get_jwt_service).

    Raises:
        HTTPException: HTTP-ошибка

    Returns:
        dict: Пару токенов
    """
    try:
        result = await user_service.authenticate(data)
    except (UserNotFoundError, PasswordVerifyError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Неверный логин или пароль'
        )
    
    tokens = await jwt_service.create_token_pair(result.id)
    return tokens


@router.post(
    '/logout',
    status_code=status.HTTP_200_OK,
    summary='Выход из аккаунта'
)
async def logout(
    token: RefreshTokenRequest, 
    jwt_service: JWTService = Depends(get_jwt_service)
) -> dict:
    """Выход пользователя из аккаунта

    Args:
        token (RefreshTokenRequest): refresh-токен
        jwt_service (JWTService, optional): Инжект jwt сервиса. Defaults to Depends(get_jwt_service).

    Raises:
        HTTPException: HTTP-ошибка

    Returns:
        dict: Ответ пользователю
    """
    
    try:
        result = await jwt_service.logout(token.refresh_token)
        return {'detail': 'Успешный выход'}
    except (TokenTypeError, LogoutError):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Ошибка выхода'
        )
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Подпись истекла'
        )


@router.post(
    '/refresh',
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
    summary='Обновление пары токенов'
)
async def refresh(
    data: RefreshTokenRequest,
    jwt_service: JWTService = Depends(get_jwt_service)
) -> dict:
    """Обновление пары токенов

    Args:
        refresh_token (RefreshTokenRequest): refresh-токен
        jwt_service (JWTService, optional): Инжект jwt сервиса. Defaults to Depends(get_jwt_service).

    Raises:
        HTTPException: HTTP-ошибка

    Returns:
        dict: Пару токенов
    """
    
    try:
        tokens = await jwt_service.refresh_tokens(data.refresh_token)
        return tokens
    except TokenCreationError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Ошибка при создании новой пары токенов'
        )
    except TokenBlaklistError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Токен недействителен'
        )
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Подпись истекла'
        )
        
    
@router.get(
    '/profile',
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary='Профиль пользователя'
)
async def profile(
    user_id: int = Depends(get_current_user),
    user_service: UserService = Depends(get_user_service)
):
    """Профиль пользователя

    Args:
        user_id: ID текущего пользователя.
        user_service: Инжект user сервиса.

    Raises:
        HTTPException: HTTP-ошибка

    Returns:
        Данные пользователя
    """
    
    try:
        user = await user_service.get_user_by_id(user_id)
        return user
    except UserNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Пользователь не найден'
        )
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Подпись истекла'
        )