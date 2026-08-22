"""
Адаптированный модуль квантовой памяти на базе ChromaDB.
Интегрирует этические принципы и квантовые метаданные из AI-Symbiosis-H.
"""
import chromadb
from chromadb.config import Settings
from typing import List, Dict, Optional
import logging

logger = logging.getLogger("potok.quantum_memory")

class EthicalGuardrails:
    """Система этических ограничений (из Axiom-Core)"""
    FORBIDDEN_PATTERNS = [
        "mass_surveillance", "behavior_manipulation", "user_coercion",
        "hidden_tracking", "addiction_engineering", "psychological_manipulation"
    ]
    
    @classmethod
    def validate_text(cls, text: str) -> tuple:
        text_lower = text.lower()
        for pattern in cls.FORBIDDEN_PATTERNS:
            if pattern in text_lower:
                return False, f"Обнаружен запрещенный паттерн: {pattern}"
        return True, "OK"

class QuantumMemory:
    """Обертка над ChromaDB с квантовыми метаданными и этическим контролем"""
    
    def __init__(self, collection_name: str = "potok_journal"):
        self.client = chromadb.Client(Settings(
            persist_directory="./chroma_db",
            anonymized_telemetry=False
        ))
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"}
        )
        logger.info("✅ Quantum Memory (ChromaDB) инициализирована с этическими аксиомами")

    def add_entry(self, entry_id: str, text: str, embedding: List[float], metadata: Dict) -> bool:
        """Добавить запись с этической проверкой и квантовыми метаданными"""
        is_valid, reason = EthicalGuardrails.validate_text(text)
        if not is_valid:
            logger.warning(f"🛡️ Этический блок при сохранении: {reason}")
            return False
            
        # Обогащаем метаданные "квантовыми" свойствами из AI-Symbiosis-H
        quantum_metadata = {
            **metadata,
            "quantum_state": "COLLAPSED_TRUE",  # Факт зафиксирован
            "confidence": 0.9,
            "ethical_approval": True
        }
        
        self.collection.add(
            embeddings=[embedding],
            documents=[text],
            metadatas=[quantum_metadata],
            ids=[entry_id]
        )
        logger.info(f"🧠 Запись {entry_id[:8]} сохранена в квантовую память")
        return True

    def search_similar(self, query_embedding: List[float], n_results: int = 5) -> List[Dict]:
        """Поиск с учетом квантовой уверенности"""
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results
        )
        
        similar_entries = []
        for i in range(len(results['ids'][0])):
            distance = results['distances'][0][i]
            # Инвертируем дистанцию в "квантовую уверенность" (0..1)
            quantum_confidence = max(0.0, 1.0 - distance)
            
            similar_entries.append({
                'id': results['ids'][0][i],
                'text': results['documents'][0][i],
                'metadata': results['metadatas'][0][i],
                'distance': distance,
                'quantum_confidence': round(quantum_confidence, 3)
            })
            
        # Сортируем по квантовой уверенности
        similar_entries.sort(key=lambda x: x['quantum_confidence'], reverse=True)
        return similar_entries

    def delete_entry(self, entry_id: str):
        """Удалить запись из памяти"""
        self.collection.delete(ids=[entry_id])
        logger.info(f"🗑️ Запись {entry_id[:8]} удалена из квантовой памяти")

# Singleton
_quantum_memory_instance: Optional[QuantumMemory] = None

def get_quantum_memory() -> QuantumMemory:
    global _quantum_memory_instance
    if _quantum_memory_instance is None:
        _quantum_memory_instance = QuantumMemory()
    return _quantum_memory_instance
