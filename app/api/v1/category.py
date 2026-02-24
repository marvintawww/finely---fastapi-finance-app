from fastapi import APIRouter, Depends, HTTPException, status
from jose import JWTError

from dependencies.category import get_category_service
from dependencies.auth import get_current_user
from schemas.category import (
    CategoryCreate,
    CategoryResponse,
    CategoryUpdate
)
from services.category import CategoryService
from utils.exceptions import (
    CategoryExistingError, 
    DeleteError,
    CategoryNotFoundError,
    NotFoundError
)


router = APIRouter(prefix='/api/v1/category')


@router.post(
    '/create',
    status_code=status.HTTP_201_CREATED,
    summary='Создание новой категории'
)
async def create_new_category(
    data: CategoryCreate,
    category_service: CategoryService = Depends(get_category_service),
    user_id: int = Depends(get_current_user)
) -> dict:
    """Создание новой категории

    Args:
        data: Данные для создания категории
        category_service: Инжект category сервиса. Defaults to Depends(get_category_service).

    Raises:
        HTTPException: HTTP-ошибка

    Returns:
        Сообщение о результате
    """
    
    try:
        category = await category_service.create_category(data, user_id)
        return {'details': 'Категория успешно создана'}
    except CategoryExistingError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Такая категория уже существует'
        )
        

@router.delete(
    '/{category_id}',
    status_code=status.HTTP_200_OK,
    summary='Удаление категории'
)
async def delete_category(
    category_id: int,
    user_id: int = Depends(get_current_user),
    category_service: CategoryService = Depends(get_category_service)
) -> dict:
    """

    Args:
        category_id: ID категории
        category_service: Инжект сервиса категории.

    Raises:
        HTTPException: HTTP-ошибка

    Returns:
        Информацию об удаление (Succes/Fail)
    """
    
    try:
        await category_service.delete_category(category_id, user_id)
        return {'detail': 'Успешное удаление категории'}
    except DeleteError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Ошибка при удалении категории'
        )
   

@router.get(
    '/',
    response_model=list[CategoryResponse],
    status_code=status.HTTP_200_OK,
    summary='Список категорий'
)
async def all_categories(
    search: str | None = None,
    category_type: str | None = None,
    skip: int = 0,
    limit: int = 10,
    user_id: int = Depends(get_current_user),
    category_service: CategoryService = Depends(get_category_service)
) -> list:
    """Список категорий
    
    Args:
        search: Текстовый поиск
        category_type: Тип категории
        skip: skip параметр, по умолчанию = 0
        limit: limit параметр, по умолчанию = 10
        user_id: ID текущего пользователя
        category_service: Сервис категорий

    Returns:
        list: Список категорий
    """
  
    categories = await category_service.get_categories(
        user_id=user_id,
        skip=skip,
        limit=limit,
        search=search,
        category_type=category_type
    )
    return categories


@router.get(
    '/{category_id}',
    response_model=CategoryResponse,
    status_code=status.HTTP_200_OK,
    summary='Категория по ID'
)
async def get_one_category(
    category_id: int,
    category_service: CategoryService = Depends(get_category_service),
    user_id: int = Depends(get_current_user)
):
    """Получаем одну категорию по ID категории и текущего пользователя

    Args:
        category_id: ID категории
        category_service: Сервис категории.
        user_id: ID текущего пользователя.

    Raises:
        HTTPException: HTTP-ошибка

    Returns:
        Данные категории
    """
    
    try:
        category = await category_service.get_category_by_user(
            category_id=category_id,
            user_id=user_id
        )
        
        return category
    except CategoryNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Категория не найдена'
        )

        
        
@router.patch(
    '/{category_id}',
    response_model=CategoryResponse,
    status_code=status.HTTP_200_OK,
    summary='Обновление имени категории'
)
async def category_name_edit(
    data: CategoryUpdate,
    category_id: int,
    user_id: int = Depends(get_current_user),
    category_service: CategoryService = Depends(get_category_service)
):
    """Обновление имени категории

    Args:
        data: Новые данные
        category_id: ID категории
        user_id: ID текущего пользователя
        category_service: Сервис категорий

    Raises:
        HTTPException: 404: Категория не найдена #!

    Returns:
        _type_: Обновленная категория
    """
    
    try:
        category = await category_service.category_update(
            data,
            user_id,
            category_id
        )
        return category
    except NotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Категория не найдена'
        )