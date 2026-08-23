import os
# Принудительно отключаем CUDA, чтобы избежать зависания при загрузке библиотек
os.environ["CUDA_VISIBLE_DEVICES"] = ""

from sentence_transformers import SentenceTransformer
from typing import List
import logging

logger = logging.getLogger("potok.embeddings")
_model = None

def get_embedding_model():
    global _model
    if _model is None:
        logger.info("Загрузка модели эмбеддингов (строго CPU mode)...")
        # Явно указываем device='cpu'
        _model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2', device='cpu')
        logger.info("✅ Модель загружена")
    return _model

def generate_embedding(text: str) -> List[float]:
    model = get_embedding_model()
    embedding = model.encode(text)
    return embedding.tolist()

def generate_embeddings(texts: List[str]) -> List[List[float]]:
    model = get_embedding_model()
    embeddings = model.encode(texts)
    return embeddings.tolist()
