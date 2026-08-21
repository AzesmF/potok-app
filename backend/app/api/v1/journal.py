"""
Роутер для работы с записями дневника.
Поддерживает два режима: journal (обычный) и flow (Поток с LLM).
"""

from fastapi import APIRouter, HTTPException, status
from datetime import datetime
from uuid import uuid4
from typing import List
from app.schemas import (
    JournalEntryRequest, JournalEntryResponse, JournalListResponse
)
from app.models.profile import get_user, create_user
from app.services.llm_service import get_llm_provider
import hashlib
import logging

router = APIRouter(prefix="/api/v1/journal", tags=["journal"])
logger = logging.getLogger("potok.journal")

# In-memory хранилище записей (MVP)
_entries_db: List[JournalEntryResponse] = []

@router.post("/entries", response_model=JournalEntryResponse, status_code=status.HTTP_201_CREATED)
async def create_entry(entry: JournalEntryRequest):
    """
    Создать запись в дневнике.
    - Режим journal: просто сохраняет текст.
    - Режим flow: активирует ИИ-обработку в духе CCF.
    """
    entry_id = str(uuid4())
    entry_date = entry.date or datetime.utcnow().isoformat()
    
    # Базовый ответ (работает в обоих режимах)
    response = JournalEntryResponse(
        id=entry_id,
        text=entry.text,
        date=entry_date,
        mode=entry.mode,
    )
    
    # Если режим flow — активируем LLM
    if entry.mode == "flow":
        # Для MVP создаём временного пользователя, если нет профиля
        # В будущем — привязка к authenticated user
        user = create_user()
        llm = get_llm_provider()
        ai_result = await llm.generate_flow_response(entry.text, user.mind_type)
        
        response.ai_response = ai_result["ai_response"]
        response.structured_tasks = ai_result["structured_tasks"]
        response.reflection_question = ai_result["reflection_question"]
        
        logger.info(f"Flow entry created. Hash: {hashlib.sha256(entry.text.encode()).hexdigest()[:8]}")
    else:
        logger.info(f"Journal entry created (plain mode).")
    
    _entries_db.append(response)
    return response

@router.get("/entries", response_model=JournalListResponse)
async def list_entries(limit: int = 50, offset: int = 0):
    """Получить список записей с пагинацией."""
    sliced = _entries_db[offset:offset + limit]
    return JournalListResponse(entries=sliced, total=len(_entries_db))

@router.get("/entries/{entry_id}", response_model=JournalEntryResponse)
async def get_entry(entry_id: str):
    """Получить одну запись по ID."""
    for entry in _entries_db:
        if entry.id == entry_id:
            return entry
    raise HTTPException(status_code=404, detail="Запись не найдена")
