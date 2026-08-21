"""
Абстракция LLM-сервиса.
В MVP — mock-реализация. В будущем — OpenAI/локальные модели.
Принцип: слабая связанность, легко заменить реализацию.
"""

from abc import ABC, abstractmethod
from typing import List, Optional
from app.core.mind_types import MindType

class LLMProvider(ABC):
    """Интерфейс для LLM-провайдера."""
    
    @abstractmethod
    async def generate_flow_response(
        self, 
        user_text: str, 
        mind_type: Optional[MindType]
    ) -> dict:
        """Генерирует ответ в режиме 'Поток' (flow)."""
        pass
    
    @abstractmethod
    async def analyze_mind_type(
        self, 
        answers: List[dict]
    ) -> dict:
        """Анализирует ответы стресс-теста и определяет тип мышления."""
        pass

class MockLLMProvider(LLMProvider):
    """Mock-реализация для MVP. Возвращает заглушки."""
    
    async def generate_flow_response(self, user_text: str, mind_type: Optional[MindType]) -> dict:
        type_context = f" (тип: {mind_type.value})" if mind_type else ""
        return {
            "ai_response": f"Я слышу тебя{type_context}. Твоя запись важна. Давай разберём её вместе в духе Поля Со-Творения.",
            "structured_tasks": [
                {"title": "Разобрать запись на ключевые темы", "priority": "high", "estimated_time_min": 15},
                {"title": "Сформулировать следующий шаг", "priority": "medium", "estimated_time_min": 10}
            ],
            "reflection_question": "Что из записанного вызывает наибольший отклик прямо сейчас?"
        }
    
    async def analyze_mind_type(self, answers: List[dict]) -> dict:
        # В MVP возвращаем аналитический тип по умолчанию
        # В будущем здесь будет реальный анализ через LLM
        return {
            "mind_type": MindType.ANALYTICAL,
            "key_patterns": [
                "Стремление к структуре и логике",
                "Предпочтение данных интуиции",
                "Мобилизация под давлением"
            ],
            "recommended_spheres": [
                {"sphere": "Системная архитектура", "reason": "Аналитический склад ума хорошо ложится на проектирование систем"},
                {"sphere": "Анализ данных", "reason": "Критерий истины — непротиворечивость"},
                {"sphere": "Управление проектами", "reason": "Структурирование хаоса"}
            ],
            "micro_step": "На этой неделе попробуй описать одну рабочую задачу в виде дерева решений (if-then).",
            "disclaimer": "Это гипотеза, а не приговор. Выбор всегда за тобой."
        }

# Singleton для MVP
_llm_instance: Optional[LLMProvider] = None

def get_llm_provider() -> LLMProvider:
    global _llm_instance
    if _llm_instance is None:
        _llm_instance = MockLLMProvider()
    return _llm_instance
