import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1 import health, journal, onboarding
from app.db.database import init_db

logger = logging.getLogger("potok.main")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # При старте
    logger.info("Инициализация базы данных...")
    await init_db()
    logger.info("✅ База данных готова")
    yield
    # При завершении (очистка ресурсов)
    logger.info("Завершение работы...")

app = FastAPI(
    title="Поток API",
    description="Пилотный проект методологии KON-MATRIX: дневник с квантовой памятью",
    version="0.2.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Регистрируем роутеры
app.include_router(journal.router, prefix="/api/v1/journal")
app.include_router(onboarding.router, prefix="/api/v1/onboarding")
app.include_router(health.router)
