"""
Абстракция LLM-сервиса.
В MVP — mock-реализация. В будущем — OpenAI/локальные модели.
Принцип: слабая связанность, легко заменить реализацию.
"""

from abc import ABC, abstractmethod

from app.core.mind_types import MindType


class LLMProvider(ABC):
    """Интерфейс для LLM-провайдера."""

    @abstractmethod
    async def generate_flow_response(self, user_text: str, mind_type: MindType | None) -> dict:
        """Генерирует ответ в режиме 'Поток' (flow)."""

    @abstractmethod
    async def analyze_mind_type(self, answers: list[dict]) -> dict:
        """Анализирует ответы стресс-теста и определяет тип мышления."""


class MockLLMProvider(LLMProvider):
    """Mock-реализация для MVP. Возвращает заглушки."""

    async def generate_flow_response(self, user_text: str, mind_type: MindType | None) -> dict:
        return {
            "ai_response": "Я тебя услышал. Давай разберём твою запись вместе и найдём важное.",
            "structured_tasks": [
                {
                    "title": "Разобрать запись на ключевые темы",
                    "priority": "high",
                    "estimated_time_min": 15,
                },
                {
                    "title": "Сформулировать следующий шаг",
                    "priority": "medium",
                    "estimated_time_min": 10,
                },
            ],
            "reflection_question": "Что из записанного вызывает наибольший отклик прямо сейчас?",
        }

    async def analyze_mind_type(self, answers: list[dict]) -> dict:
        return {
            "mind_type": MindType.ANALYTICAL,
            "key_patterns": [
                "Стремление к структуре и логике",
                "Предпочтение данных интуиции",
                "Мобилизация под давлением",
            ],
            "recommended_spheres": [
                {
                    "sphere": "Системная архитектура",
                    "reason": "Аналитический склад ума хорошо ложится на проектирование систем",
                },
                {
                    "sphere": "Анализ данных",
                    "reason": "Критерий истины — непротиворечивость",
                },
                {"sphere": "Управление проектами", "reason": "Структурирование хаоса"},
            ],
            "micro_step": "На этой неделе попробуй описать одну рабочую задачу в виде дерева решений (if-then).",
            "disclaimer": "Это гипотеза, а не приговор. Выбор всегда за тобой.",
        }


_llm_instance: LLMProvider | None = None


def get_llm_provider() -> LLMProvider:
    global _llm_instance
    if _llm_instance is None:
        _llm_instance = MockLLMProvider()
    return _llm_instance
