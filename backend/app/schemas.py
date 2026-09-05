"""
Pydantic схемы для валидации запросов и ответов API.
"""

from pydantic import BaseModel, Field

# ==========================================
# Journal Schemas
# ==========================================


class TaskItem(BaseModel):
    title: str
    priority: str  # "high", "medium", "low"
    estimated_time_min: int


class JournalEntryRequest(BaseModel):
    text: str = Field(..., min_length=1, description="Текст записи")
    mode: str = Field(default="journal", description="Режим: 'journal' или 'flow'")
    date: str | None = None


class JournalEntryResponse(BaseModel):
    id: str
    text: str
    date: str
    mode: str
    ai_response: str | None = None
    structured_tasks: list[TaskItem] | None = None
    reflection_question: str | None = None


class JournalListResponse(BaseModel):
    entries: list[JournalEntryResponse]
    total: int


# ==========================================
# Onboarding / Profile Schemas
# ==========================================


class StressTestStartResponse(BaseModel):
    user_id: str
    questions: list[str]
    total_questions: int


class StressTestAnswerRequest(BaseModel):
    user_id: str
    question_index: int
    answer: str


class RecommendedSphere(BaseModel):
    sphere: str
    reason: str


class StressTestCompleteResponse(BaseModel):
    mind_type: str
    mind_type_description: str
    key_patterns: list[str]
    recommended_spheres: list[RecommendedSphere]
    micro_step: str
    disclaimer: str


class MindTypeResponse(BaseModel):
    user_id: str
    mind_type: str | None
    created_at: str | None
