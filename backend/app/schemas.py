"""
Pydantic схемы для валидации запросов и ответов API.
"""

from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

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
    date: Optional[str] = None

class JournalEntryResponse(BaseModel):
    id: str
    text: str
    date: str
    mode: str
    ai_response: Optional[str] = None
    structured_tasks: Optional[List[TaskItem]] = None
    reflection_question: Optional[str] = None

class JournalListResponse(BaseModel):
    entries: List[JournalEntryResponse]
    total: int

# ==========================================
# Onboarding / Profile Schemas
# ==========================================

class StressTestStartResponse(BaseModel):
    user_id: str
    questions: List[str]
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
    key_patterns: List[str]
    recommended_spheres: List[RecommendedSphere]
    micro_step: str
    disclaimer: str

class MindTypeResponse(BaseModel):
    user_id: str
    mind_type: Optional[str]
    created_at: Optional[str]
