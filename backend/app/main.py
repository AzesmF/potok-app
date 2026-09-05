"""
Главный файл приложения FastAPI.
Инициализирует базу данных при старте.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

from app.api.v1 import journal, onboarding
from app.api.v1 import health
from app.db.database import init_db

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

# Lifespan контекст (инициализация при старте)
@asynccontextmanager
async def lifespan(app: FastAPI):
    # При старте
    logging.info("Инициализация базы данных...")
    await init_db()
    logging.info("✅ База данных готова")
    yield
    # При завершении (очистка ресурсов)
    logging.info("Завершение работы...")

app = FastAPI(
    title="Поток API",
    description="API для приложения «Поток» - отвечающий дневник с ИИ",
    version="0.2.0",
    lifespan=lifespan
)

# CORS для Flutter
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем роутеры
app.include_router(journal.router)
app.include_router(onboarding.router)
app.include_router(health.router)

@app.get("/")
async def root():
    return {
        "message": "Поток API работает",
        "version": "0.2.0",
        "modes": ["journal", "flow"],
        "database": "SQLite + ChromaDB"
    }
