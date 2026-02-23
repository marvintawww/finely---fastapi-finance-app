from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from database.db import db
from api.v1.user import router as user_router
from api.v1.category import router as category_router
from api.v1.transaction import router as transaction_router
from api.v1.statistics import router as stat_router

#! === Добавлять импорт моделей в main === !#
from models.user import User
from models.category import Category
from models.token import TokenBlacklist
from models.transaction import Transaction

@asynccontextmanager
async def lifespan(app: FastAPI):
    await db.create_tables()
    yield
    await db.engine.dispose()
    
app = FastAPI(
    title='Finance App',
    description='App for finance management',
    version='0.0.1',
    lifespan=lifespan
)

# CORS middleware для работы с фронтендом
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # В продакшене указать конкретные домены
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router)
app.include_router(category_router)
app.include_router(transaction_router)
app.include_router(stat_router)

@app.get('/')
async def health():
    return {'status': 'healthy'}