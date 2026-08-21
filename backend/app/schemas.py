"""
Pydantic схемы для API контрактов.
Разделены по доменам: journal, onboarding, profile.
"""

from pydantic import BaseModel, Field
from typing import List, Optional
from app.core.mind_types import MindType

# === Journal (Дневник) ===

class JournalEntryRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=10000, description="Текст записи")
    mode: str = Field(default="journal", description="Режим: journal (обычный) или flow (Поток с LLM)")
    date: Optional[str] = Field(None, description="Дата записи (ISO формат). Если не указана — сегодня.")

class JournalEntryResponse(BaseModel):
    id: str
    text: str
    date: str
    mode: str
    # Поля заполняются только в режиме flow
    ai_response: Optional[str] = None
    structured_tasks: Optional[List[dict]] = None
    reflection_question: Optional[str] = None

class JournalListResponse(BaseModel):
    entries: List[JournalEntryResponse]
    total: int

# === Onboarding (Определение типа мышления) ===

class StressTestStartResponse(BaseModel):
    user_id: str
    questions: List[str]
    total_questions: int

class StressTestAnswerRequest(BaseModel):
    user_id: str
    question_index: int
    answer: str

class StressTestResultResponse(BaseModel):
    user_id: str
    mind_type: str
    mind_type_description: str
    key_patterns: List[str]
    recommended_spheres: List[dict]
    micro_step: str
    disclaimer: str

# === Profile ===

class UserProfileResponse(BaseModel):
    user_id: str
    mind_type: Optional[str]
    stress_test_completed: bool
    active_mode: str
