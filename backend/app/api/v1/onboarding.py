"""
Роутер онбординга: определение типа мышления через стресс-тест.
Следует принципам CCF: без манипуляций, гипотеза а не приговор.
"""

from fastapi import APIRouter, HTTPException, status
from app.schemas import (
    StressTestStartResponse, StressTestAnswerRequest, StressTestResultResponse
)
from app.core.mind_types import (
    STRESS_TEST_QUESTIONS, QUESTIONS_PER_TYPE, 
    MIND_TYPE_DESCRIPTIONS, MindType
)
from app.models.profile import get_user, create_user, update_user
from app.services.llm_service import get_llm_provider
import logging

router = APIRouter(prefix="/api/v1/onboarding", tags=["onboarding"])
logger = logging.getLogger("potok.onboarding")

@router.post("/stress-test/start", response_model=StressTestStartResponse)
async def start_stress_test(user_id: str = None):
    """
    Начать стресс-тест для определения типа мышления.
    Возвращает первые вопросы.
    """
    if user_id:
        user = get_user(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="Пользователь не найден")
    else:
        user = create_user()
    
    questions = STRESS_TEST_QUESTIONS[:QUESTIONS_PER_TYPE]
    
    logger.info(f"Stress test started for user {user.id}")
    
    return StressTestStartResponse(
        user_id=user.id,
        questions=questions,
        total_questions=len(questions)
    )

@router.post("/stress-test/answer", status_code=status.HTTP_200_OK)
async def submit_answer(payload: StressTestAnswerRequest):
    """
    Сохранить ответ на вопрос стресс-теста.
    """
    user = get_user(payload.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    
    if payload.question_index < 0 or payload.question_index >= QUESTIONS_PER_TYPE:
        raise HTTPException(status_code=400, detail="Неверный индекс вопроса")
    
    # Сохраняем ответ
    user.stress_test_answers.append({
        "question_index": payload.question_index,
        "answer": payload.answer
    })
    update_user(user)
    
    return {"status": "ok", "answers_count": len(user.stress_test_answers)}

@router.post("/stress-test/complete", response_model=StressTestResultResponse)
async def complete_stress_test(user_id: str):
    """
    Завершить стресс-тест и получить результат.
    В MVP использует mock-анализ. В будущем — реальный LLM-анализ.
    """
    user = get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    
    if len(user.stress_test_answers) < QUESTIONS_PER_TYPE:
        raise HTTPException(
            status_code=400, 
            detail=f"Недостаточно ответов. Нужно {QUESTIONS_PER_TYPE}, получено {len(user.stress_test_answers)}"
        )
    
    llm = get_llm_provider()
    analysis = await llm.analyze_mind_type(user.stress_test_answers)
    
    # Сохраняем результат в профиль
    user.mind_type = analysis["mind_type"]
    user.stress_test_completed = True
    update_user(user)
    
    logger.info(f"Stress test completed for user {user_id}. Type: {analysis['mind_type'].value}")
    
    return StressTestResultResponse(
        user_id=user_id,
        mind_type=analysis["mind_type"].value,
        mind_type_description=MIND_TYPE_DESCRIPTIONS[analysis["mind_type"]],
        key_patterns=analysis["key_patterns"],
        recommended_spheres=analysis["recommended_spheres"],
        micro_step=analysis["micro_step"],
        disclaimer=analysis["disclaimer"]
    )
