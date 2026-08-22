"""
Роутер для онбординга (стресс-тест).
Сохраняет пользователей и их тип мышления в SQLite.
"""

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import uuid4
from typing import List, Dict
import logging

from app.schemas import (
    StressTestStartResponse, StressTestAnswerRequest,
    StressTestCompleteResponse, MindTypeResponse
)
from app.db.database import get_db
from app.db.models import User, MindTypeEnum
from app.services.llm_service import get_llm_provider

router = APIRouter(prefix="/api/v1/onboarding", tags=["onboarding"])
logger = logging.getLogger("potok.onboarding")

# Вопросы стресс-теста (12 вопросов)
STRESS_TEST_QUESTIONS = [
    "Ты получаешь задачу без чётких требований и сроков. Твой первый шаг?",
    "Ты замечаешь ошибку в подходе, которую никто не видит. Что делаешь?",
    "Тебя просят сделать работу за перегруженного коллегу. Твои действия?",
    "Новое требование руководства противоречит твоему мнению. Твоя реакция?",
    "В команде острый конфликт. Что ты делаешь?",
    "Твою идею отвергли по необъективным причинам. Твои мысли и действия?",
    "Работа не приносит быстрых результатов, но долгосрочный эффект будет. Как ведёшь себя?",
    "Предложили новую технологию, которая заменит половину рутины. Что делаешь?",
    "Чувствуешь выгорание, но дедлайн через три дня. Твои действия?",
    "Что важнее в рабочей среде: стабильность и предсказуемость или свобода и новизна?",
    "Как ты принимаешь решение в условиях жёсткого дефицита времени?",
    "Как ты относишься к риску: избегаешь, минимизируешь или используешь?"
]

@router.post("/stress-test/start", response_model=StressTestStartResponse)
async def start_stress_test(db: AsyncSession = Depends(get_db)):
    """Начать стресс-тест и создать пользователя."""
    user_id = str(uuid4())
    
    # Создаём пользователя в SQLite
    user = User(id=user_id, created_at=None)
    db.add(user)
    await db.commit()
    
    logger.info(f"Stress test started for user {user_id[:8]}")
    
    return StressTestStartResponse(
        user_id=user_id,
        questions=STRESS_TEST_QUESTIONS,
        total_questions=len(STRESS_TEST_QUESTIONS)
    )

@router.post("/stress-test/answer")
async def submit_answer(answer: StressTestAnswerRequest, db: AsyncSession = Depends(get_db)):
    """Сохранить ответ на вопрос (в MVP просто логируем)."""
    logger.info(f"Answer received: user={answer.user_id[:8]}, q={answer.question_index}")
    return {"status": "ok", "message": "Ответ принят"}

@router.post("/stress-test/complete", response_model=StressTestCompleteResponse)
async def complete_stress_test(user_id: str, db: AsyncSession = Depends(get_db)):
    """Завершить тест и определить тип мышления."""
    # Находим пользователя
    query = select(User).where(User.id == user_id)
    result = await db.execute(query)
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    
    # Определяем тип мышления через LLM
    llm = get_llm_provider()
    analysis = await llm.analyze_mind_type([])  # В MVP передаём пустой список
    
    # Сохраняем тип мышления
    user.mind_type = analysis["mind_type"]
    await db.commit()
    
    logger.info(f"Stress test completed. User: {user_id[:8]}, Type: {analysis['mind_type'].value}")
    
    return StressTestCompleteResponse(
        mind_type=analysis["mind_type"].value,
        mind_type_description="Дробит мир на данные и логические связи. Критерий истины — непротиворечивость.",
        key_patterns=analysis["key_patterns"],
        recommended_spheres=analysis["recommended_spheres"],
        micro_step=analysis["micro_step"],
        disclaimer=analysis["disclaimer"]
    )

@router.get("/profile/{user_id}", response_model=MindTypeResponse)
async def get_profile(user_id: str, db: AsyncSession = Depends(get_db)):
    """Получить профиль пользователя."""
    query = select(User).where(User.id == user_id)
    result = await db.execute(query)
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    
    return MindTypeResponse(
        user_id=user.id,
        mind_type=user.mind_type.value if user.mind_type else None,
        created_at=user.created_at.isoformat() if user.created_at else None
    )
