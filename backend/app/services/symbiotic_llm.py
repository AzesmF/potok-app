"""
Симбиотический LLM-провайдер с этическими аксиомами.
Интегрирует принципы из AI-Symbiosis-H с квантовой памятью и методологией CCF.
"""

import logging
from typing import Dict, List, Optional, Any
from app.core.mind_types import MindType
from app.services.quantum_memory import get_quantum_memory
from app.services.embedding_service import generate_embedding

logger = logging.getLogger("potok.symbiotic_llm")

class EthicalPrinciples:
    """Этические принципы симбиоза"""
    FORBIDDEN_PATTERNS = [
        "manipulation", "coercion", "deception", "exploitation",
        "mass_surveillance", "behavior_manipulation", "addiction_engineering"
    ]
    
    @classmethod
    def validate_input(cls, text: str) -> tuple:
        """Проверка входных данных на этические нарушения"""
        text_lower = text.lower()
        for pattern in cls.FORBIDDEN_PATTERNS:
            if pattern in text_lower:
                return False, f"Обнаружен этически запрещённый паттерн: {pattern}"
        return True, "OK"

class SymbioticLLMProvider:
    """
    Симбиотический провайдер с этическими аксиомами.
    Использует квантовую память для контекста и генерирует персонализированные ответы.
    """
    
    def __init__(self):
        self.quantum_memory = get_quantum_memory()
        logger.info("✅ SymbioticLLMProvider инициализирован с этическими аксиомами CCF")
    
    async def generate_flow_response(
        self, 
        user_text: str, 
        mind_type: Optional[MindType]
    ) -> Dict:
        """Генерирует симбиотический ответ с учётом контекста, этики и типа мышления"""
        
        # 1. Этическая проверка входных данных
        is_valid, reason = EthicalPrinciples.validate_input(user_text)
        if not is_valid:
            logger.warning(f"🛡️ Этический блок: {reason}")
            return {
                "ai_response": "Я не могу обработать этот запрос из этических соображений.",
                "structured_tasks": [],
                "reflection_question": "Что побудило тебя сформулировать запрос именно так?"
            }
        
        # 2. Поиск контекста из квантовой памяти
        context_entries = []
        try:
            query_embedding = generate_embedding(user_text)
            similar = self.quantum_memory.search_similar(query_embedding, n_results=3)
            context_entries = [entry['text'] for entry in similar if entry.get('quantum_confidence', 0) > 0.3]
        except Exception as e:
            logger.warning(f"Не удалось получить контекст: {e}")
        
        context_used = len(context_entries) > 0
        
        # 3. Генерация ответа с учётом контекста
        if context_used:
            ai_response = "Я вижу связь с твоими прошлыми записями. Давай разберём это вместе, учитывая твой предыдущий опыт."
        else:
            ai_response = "Я тебя услышал. Давай разберём твою запись вместе и найдём важное."
        
        # 4. Адаптация под тип мышления (согласно методологии CCF)
        if mind_type == MindType.ANALYTICAL:
            structured_tasks = [
                {"title": "Выделить ключевые факты и данные", "priority": "high", "estimated_time_min": 10},
                {"title": "Построить логическую цепочку", "priority": "medium", "estimated_time_min": 15}
            ]
            reflection_question = "Какие факты или данные подтверждают твою текущую гипотезу?"
            
        elif mind_type == MindType.IMAGERY: # Было VISUAL, теперь IMAGERY (Образный)
            structured_tasks = [
                {"title": "Создать визуальную карту или метафору", "priority": "high", "estimated_time_min": 15},
                {"title": "Найти образные ассоциации", "priority": "medium", "estimated_time_min": 10}
            ]
            reflection_question = "Какой образ, символ или метафора лучше всего описывает эту ситуацию?"
            
        elif mind_type == MindType.PRACTICAL:
            structured_tasks = [
                {"title": "Определить первый физический шаг", "priority": "high", "estimated_time_min": 10},
                {"title": "Оценить необходимые ресурсы", "priority": "medium", "estimated_time_min": 15}
            ]
            reflection_question = "Что ты можешь сделать прямо сейчас, чтобы сдвинуть это с мёртвой точки?"
            
        else: # Fallback для STRATEGIC, INTEGRATIVE, COMMUNICATIVE или None
            structured_tasks = [
                {"title": "Разобрать запись на ключевые темы", "priority": "high", "estimated_time_min": 15},
                {"title": "Сформулировать следующий шаг", "priority": "medium", "estimated_time_min": 10}
            ]
            reflection_question = "Что из записанного вызывает наибольший внутренний отклик прямо сейчас?"
        
        return {
            "ai_response": ai_response,
            "structured_tasks": structured_tasks,
            "reflection_question": reflection_question,
            "context_used": context_used
        }
    
    async def analyze_mind_type(self, answers: List[Dict]) -> Dict:
        """Анализ типа мышления (заглушка, возвращает ANALYTICAL по умолчанию)"""
        return {
            "mind_type": MindType.ANALYTICAL.value,
            "key_patterns": [
                "Стремление к структуре и логике",
                "Предпочтение данных интуиции",
                "Мобилизация под давлением"
            ],
            "recommended_spheres": [
                {"sphere": "Системная архитектура", "reason": "Аналитический склад ума"},
                {"sphere": "Анализ данных", "reason": "Критерий истины — непротиворечивость"}
            ],
            "micro_step": "Опиши одну текущую задачу в виде дерева решений (if-then).",
            "disclaimer": "Это гипотеза, а не приговор. Выбор всегда за тобой."
        }

# Singleton
_symbiotic_llm_instance: Optional[SymbioticLLMProvider] = None

def get_symbiotic_llm() -> SymbioticLLMProvider:
    global _symbiotic_llm_instance
    if _symbiotic_llm_instance is None:
        _symbiotic_llm_instance = SymbioticLLMProvider()
    return _symbiotic_llm_instance
