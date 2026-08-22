"""
Модели таблиц для SQLite.
User - пользователь
JournalEntry - запись дневника
"""

from sqlalchemy import Column, String, DateTime, Text, Enum as SQLEnum
from sqlalchemy.sql import func
from app.db.database import Base
import enum

class MindTypeEnum(str, enum.Enum):
    ANALYTICAL = "analytical"
    VISUAL = "visual"
    KINESTHETIC = "kinesthetic"
    AUDITORY = "auditory"
    INTUITIVE = "intuitive"
    PRACTICAL = "practical"

class User(Base):
    __tablename__ = "users"
    
    id = Column(String, primary_key=True, index=True)
    mind_type = Column(SQLEnum(MindTypeEnum), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class JournalEntry(Base):
    __tablename__ = "journal_entries"
    
    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, index=True, nullable=True)
    text = Column(Text, nullable=False)
    mode = Column(String, nullable=False, default="journal")  # journal или flow
    ai_response = Column(Text, nullable=True)
    structured_tasks = Column(Text, nullable=True)  # JSON строка
    reflection_question = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
