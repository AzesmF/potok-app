"""
Векторное хранилище на базе ChromaDB.
Хранит эмбеддинги записей для семантического поиска.
"""

import chromadb
from chromadb.config import Settings


class VectorStore:
    def __init__(self, collection_name: str = "journal_entries"):
        # Инициализируем ChromaDB (persist_directory - папка для хранения)
        self.client = chromadb.Client(Settings(persist_directory="./chroma_db", anonymized_telemetry=False))

        # Получаем или создаём коллекцию
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"},  # Косинусное расстояние для похожести
        )

    def add_entry(self, entry_id: str, text: str, embedding: list[float], metadata: dict):
        """Добавить запись в векторное хранилище."""
        self.collection.add(
            embeddings=[embedding],
            documents=[text],
            metadatas=[metadata],
            ids=[entry_id],
        )

    def search_similar(self, query_embedding: list[float], n_results: int = 5) -> list[dict]:
        """Найти похожие записи по эмбеддингу запроса."""
        results = self.collection.query(query_embeddings=[query_embedding], n_results=n_results)

        # Форматируем результаты
        similar_entries = []
        for i in range(len(results["ids"][0])):
            similar_entries.append(
                {
                    "id": results["ids"][0][i],
                    "text": results["documents"][0][i],
                    "metadata": results["metadatas"][0][i],
                    "distance": results["distances"][0][i],
                }
            )

        return similar_entries

    def delete_entry(self, entry_id: str):
        """Удалить запись из векторного хранилища."""
        self.collection.delete(ids=[entry_id])

    def get_entry(self, entry_id: str) -> dict | None:
        """Получить запись по ID."""
        result = self.collection.get(ids=[entry_id])
        if result["ids"]:
            return {
                "id": result["ids"][0],
                "text": result["documents"][0],
                "metadata": result["metadatas"][0],
            }
        return None


# Singleton
_vector_store_instance: VectorStore | None = None


def get_vector_store() -> VectorStore:
    global _vector_store_instance
    if _vector_store_instance is None:
        _vector_store_instance = VectorStore()
    return _vector_store_instance
