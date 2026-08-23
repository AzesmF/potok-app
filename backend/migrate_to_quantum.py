"""
Миграция: добавить существующие записи из SQLite в квантовую память (ChromaDB).
"""
import asyncio
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.db.database import AsyncSessionLocal
from app.db.models import JournalEntry
from app.services.quantum_memory import get_quantum_memory
from app.services.embedding_service import generate_embedding
from sqlalchemy import select
import json

async def migrate_entries_to_quantum_memory():
    print("Начинаем миграцию записей в квантовую память...")
    
    async with AsyncSessionLocal() as session:
        query = select(JournalEntry)
        result = await session.execute(query)
        entries = result.scalars().all()
        
        print(f"Найдено записей в SQLite: {len(entries)}")
        
        quantum_memory = get_quantum_memory()
        migrated_count = 0
        
        for entry in entries:
            existing = quantum_memory.collection.get(ids=[entry.id])
            if existing['ids']:
                print(f"Запись {entry.id[:8]} уже есть в квантовой памяти")
                continue
            
            print(f"Обрабатываем запись {entry.id[:8]}: {entry.text[:50]}...")
            embedding = generate_embedding(entry.text)
            
            success = quantum_memory.add_entry(
                entry_id=entry.id,
                text=entry.text,
                embedding=embedding,
                metadata={
                    "mode": entry.mode,
                    "date": entry.created_at.isoformat() if entry.created_at else "",
                    "has_ai_response": entry.ai_response is not None
                }
            )
            
            if success:
                migrated_count += 1
                print(f"Запись {entry.id[:8]} добавлена в квантовую память")
            else:
                print(f"Запись {entry.id[:8]} не прошла этический фильтр")
        
        print(f"\nМиграция завершена! Перенесено записей: {migrated_count}/{len(entries)}")

if __name__ == "__main__":
    asyncio.run(migrate_entries_to_quantum_memory())
