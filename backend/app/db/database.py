"""
Инициализация SQLite базы данных.
Используем SQLAlchemy для асинхронной работы.
"""

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

# URL базы данных (файл поток.db в корне backend)
DATABASE_URL = "sqlite+aiosqlite:///./поток.db"

# Создаём асинхронный движок
engine = create_async_engine(
    DATABASE_URL,
    echo=False,  # True для отладки SQL-запросов
    future=True
)

# Сессия для работы с БД
AsyncSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Базовый класс для моделей
Base = declarative_base()

# Функция для получения сессии
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

# Функция для создания таблиц (вызывается при старте)
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
