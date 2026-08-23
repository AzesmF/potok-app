"""
Роутер для работы с записями дневника.
Использует SQLite для хранения и ChromaDB для векторного поиска.
"""

from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime
from uuid import uuid4
from typing import List, Optional
import json

from app.schemas import (
    JournalEntryRequest, JournalEntryResponse, JournalListResponse
)
from app.db.database import get_db
from app.db.models import JournalEntry
from app.services.quantum_memory import get_quantum_memory
from app.services.llm_service import get_llm_provider
from app.services.embedding_service import generate_embedding
import logging

router = APIRouter(prefix="/api/v1/journal", tags=["journal"])
logger = logging.getLogger("potok.journal")

@router.post("/entries", response_model=JournalEntryResponse, status_code=status.HTTP_201_CREATED)
async def create_entry(entry: JournalEntryRequest, db: AsyncSession = Depends(get_db)):
    """Создать запись в дневнике с сохранением в SQLite и ChromaDB."""
    entry_id = str(uuid4())
    entry_date = entry.date or datetime.utcnow().isoformat()
    
    response = JournalEntryResponse(
        id=entry_id,
        text=entry.text,
        date=entry_date,
        mode=entry.mode,
    )
    
    # Если режим flow - активируем ИИ
    if entry.mode == "flow":
        llm = get_llm_provider()
        ai_result = await llm.generate_flow_response(entry.text, None)
        
        response.ai_response = ai_result["ai_response"]
        response.structured_tasks = ai_result["structured_tasks"]
        response.reflection_question = ai_result["reflection_question"]
        
        logger.info(f"Flow entry created. ID: {entry_id[:8]}")
    else:
        logger.info(f"Journal entry created (plain mode). ID: {entry_id[:8]}")
    
    # Сохраняем в SQLite
    db_entry = JournalEntry(
        id=entry_id,
        text=entry.text,
        mode=entry.mode,
        ai_response=response.ai_response,
        structured_tasks=json.dumps(response.structured_tasks) if response.structured_tasks else None,
        reflection_question=response.reflection_question,
        created_at=datetime.utcnow()
    )
    db.add(db_entry)
    await db.commit()
    await db.refresh(db_entry)
    
    # Сохраняем в ChromaDB (векторный поиск)
    try:
        quantum_memory = get_quantum_memory()
        embedding = generate_embedding(entry.text)
        quantum_memory.add_entry(
            entry_id=entry_id,
            text=entry.text,
            embedding=embedding,
            metadata={
                "mode": entry.mode,
                "date": entry_date,
                "has_ai_response": entry.mode == "flow"
            }
        )
        logger.info(f"Entry added to quantum memory. ID: {entry_id[:8]}")
    except Exception as e:
        logger.error(f"Failed to add to quantum memory: {e}")
    
    return response

@router.get("/entries", response_model=JournalListResponse)
async def list_entries(limit: int = 50, offset: int = 0, db: AsyncSession = Depends(get_db)):
    """Получить список записей из SQLite."""
    query = select(JournalEntry).order_by(JournalEntry.created_at.desc()).limit(limit).offset(offset)
    result = await db.execute(query)
    entries = result.scalars().all()
    
    response_entries = []
    for entry in entries:
        response_entries.append(JournalEntryResponse(
            id=entry.id,
            text=entry.text,
            date=entry.created_at.isoformat() if entry.created_at else "",
            mode=entry.mode,
            ai_response=entry.ai_response,
            structured_tasks=json.loads(entry.structured_tasks) if entry.structured_tasks else None,
            reflection_question=entry.reflection_question
        ))
    
    return JournalListResponse(entries=response_entries, total=len(response_entries))

@router.get("/entries/{entry_id}", response_model=JournalEntryResponse)
async def get_entry(entry_id: str, db: AsyncSession = Depends(get_db)):
    """Получить одну запись по ID."""
    query = select(JournalEntry).where(JournalEntry.id == entry_id)
    result = await db.execute(query)
    entry = result.scalar_one_or_none()
    
    if not entry:
        raise HTTPException(status_code=404, detail="Запись не найдена")
    
    return JournalEntryResponse(
        id=entry.id,
        text=entry.text,
        date=entry.created_at.isoformat() if entry.created_at else "",
        mode=entry.mode,
        ai_response=entry.ai_response,
        structured_tasks=json.loads(entry.structured_tasks) if entry.structured_tasks else None,
        reflection_question=entry.reflection_question
    )

@router.delete("/entries/{entry_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_entry(entry_id: str, db: AsyncSession = Depends(get_db)):
    """Удалить запись из SQLite и ChromaDB."""
    # Удаляем из SQLite
    query = select(JournalEntry).where(JournalEntry.id == entry_id)
    result = await db.execute(query)
    entry = result.scalar_one_or_none()
    
    if not entry:
        raise HTTPException(status_code=404, detail="Запись не найдена")
    
    await db.delete(entry)
    await db.commit()
    
    # Удаляем из ChromaDB
    try:
        quantum_memory = get_quantum_memory()
        quantum_memory.delete_entry(entry_id)
        logger.info(f"Entry deleted from SQLite and quantum memory. ID: {entry_id[:8]}")
    except Exception as e:
        logger.error(f"Failed to delete from quantum memory: {e}")
    
    return None

@router.get("/search")
async def search_entries(query: str, limit: int = 5):
    """Семантический поиск по записям через ChromaDB."""
    try:
        quantum_memory = get_quantum_memory()
        query_embedding = generate_embedding(query)
        similar = quantum_memory.search_similar(query_embedding, n_results=limit)
        
        return {"results": similar, "total": len(similar)}
    except Exception as e:
        logger.error(f"Search failed: {e}")
        raise HTTPException(status_code=500, detail="Поиск не удался")
