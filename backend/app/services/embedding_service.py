"""
Сервис генерации эмбеддингов через sentence-transformers.
Используем локальную модель (не требует API ключей).
"""

from sentence_transformers import SentenceTransformer
from typing import List
import logging

logger = logging.getLogger("potok.embeddings")

# Глобальная переменная для модели (ленивая загрузка)
_model = None

def get_embedding_model():
    """Получить модель эмбеддингов (ленивая загрузка)."""
    global _model
    if _model is None:
        logger.info("Загрузка модели эмбеддингов (первый запуск может занять время)...")
        # Используем мультиязычную модель (поддерживает русский)
        _model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
        logger.info("✅ Модель загружена")
    return _model

def generate_embedding(text: str) -> List[float]:
    """Сгенерировать эмбеддинг для текста."""
    model = get_embedding_model()
    embedding = model.encode(text)
    return embedding.tolist()

def generate_embeddings(texts: List[str]) -> List[List[float]]:
    """Сгенерировать эмбеддинги для списка текстов."""
    model = get_embedding_model()
    embeddings = model.encode(texts)
    return embeddings.tolist()
