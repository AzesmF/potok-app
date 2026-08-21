"""
Главный файл приложения Поток.
Подключает все роутеры и настраивает middleware.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1 import journal, onboarding, profile
from app.core.config import settings
import logging

# Настройка логирования (Принцип Прозрачности)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

app = FastAPI(
    title=settings.app_name,
    description="Приложение-дневник с режимами: обычный и Поток (CCF)",
    version=settings.version
)

# CORS для кроссплатформенного клиента
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # В продакшене — конкретные домены
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключение роутеров
app.include_router(journal.router)
app.include_router(onboarding.router)
app.include_router(profile.router)

@app.get("/")
async def root():
    return {
        "message": "Поток API работает",
        "version": settings.version,
        "modes": settings.available_modes
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
