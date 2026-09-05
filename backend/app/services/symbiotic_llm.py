"""
Симбиотический LLM-провайдер с этическими аксиомами.
Интегрирует принципы из AI-Symbiosis-H с квантовой памятью и методологией CCF.
Стандарт INT-L3: Использование версионированных промптов.
"""

import logging
from typing import Dict, List, Optional, Any
from app.core.mind_types import MindType
from app.core.prompts import FLOW_RESPONSE_TEMPLATES, REFLECTION_QUESTIONS
from app.services.quantum_memory import get_quantum_memory
from app.services.embedding_service import generate_embedding
from app.services.worm_logger import get_worm_logger

logger = logging.getLogger("potok.symbiotic_llm")

class EthicalPrinciples:
    """Этические принципы симбиоза"""
    FORBIDDEN_PATTERNS = [
        "manipulation", "coercion", "deception", "exploitation",
        "mass_surveillance", "behavior_manipulation", "addiction_engineering"
    ]
    
    @classmethod
    def validate_input(cls, text: str) -> tuple:
        text_lower = text.lower()
        for pattern in cls.FORBIDDEN_PATTERNS:
            if pattern in text_lower:
                return False, f"Обнаружен этически запрещённый паттерн: {pattern}"
        return True, "OK"

class SymbioticLLMProvider:
    def __init__(self):
        self.quantum_memory = get_quantum_memory()
        self.worm_logger = get_worm_logger()
        logger.info("✅ SymbioticLLMProvider инициализирован с этическими аксиомами CCF и WORM-аудитом")
    
    async def generate_flow_response(self, user_text: str, mind_type: Optional[MindType]) -> Dict:
        # 1. Этическая проверка
        is_valid, reason = EthicalPrinciples.validate_input(user_text)
        if not is_valid:
            self.worm_logger.log("ethical_block", {"reason": reason}, ethical_score=0.0)
            return {
                "ai_response": FLOW_RESPONSE_TEMPLATES["ethical_block"],
                "structured_tasks": [],
                "reflection_question": "Что побудило тебя сформулировать запрос именно так?"
            }
        
        # 2. Поиск контекста
        context_used = False
        try:
            query_embedding = generate_embedding(user_text)
            similar = self.quantum_memory.search_similar(query_embedding, n_results=3)
            context_used = any(entry.get('quantum_confidence', 0) > 0.3 for entry in similar)
        except Exception as e:
            logger.warning(f"Не удалось получить контекст: {e}")
        
        # 3. Генерация ответа через версионированные шаблоны
        template_key = "context_aware" if context_used else "default"
        ai_response = FLOW_RESPONSE_TEMPLATES[template_key]
        
        # 4. Адаптация под тип мышления
        mind_type_str = mind_type.value if mind_type else "default"
        reflection_question = REFLECTION_QUESTIONS.get(mind_type_str, REFLECTION_QUESTIONS["default"])
        
        structured_tasks = [
            {"title": "Разобрать запись на ключевые темы", "priority": "high", "estimated_time_min": 15},
            {"title": "Сформулировать следующий шаг", "priority": "medium", "estimated_time_min": 10}
        ]
        
        # 5. Логируем успешную операцию в WORM (только метаданные!)
        self.worm_logger.log(
            "flow_response_generated", 
            {
                "mind_type": mind_type_str,
                "context_used": context_used,
                "template_version": "1.0.0" # Ссылка на версию промпта
            }, 
            ethical_score=1.0
        )
        
        return {
            "ai_response": ai_response,
            "structured_tasks": structured_tasks,
            "reflection_question": reflection_question,
            "context_used": context_used
        }

# Singleton
_symbiotic_llm_instance: Optional[SymbioticLLMProvider] = None

def get_symbiotic_llm() -> SymbioticLLMProvider:
    global _symbiotic_llm_instance
    if _symbiotic_llm_instance is None:
        _symbiotic_llm_instance = SymbioticLLMProvider()
    return _symbiotic_llm_instance
