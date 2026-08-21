"""
Модель профиля пользователя.
В MVP — in-memory хранилище. В будущем — PostgreSQL.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List
from uuid import uuid4
from app.core.mind_types import MindType

@dataclass
class UserProfile:
    id: str = field(default_factory=lambda: str(uuid4()))
    created_at: datetime = field(default_factory=datetime.utcnow)
    mind_type: Optional[MindType] = None
    stress_test_completed: bool = False
    stress_test_answers: List[dict] = field(default_factory=list)
    # Расширяемость: future modes (КПО, MAS CCF) будут добавляться сюда
    active_mode: str = "journal"  # journal | flow | future modes

# In-memory хранилище (MVP)
_users_db: dict[str, UserProfile] = {}

def get_user(user_id: str) -> Optional[UserProfile]:
    return _users_db.get(user_id)

def create_user() -> UserProfile:
    user = UserProfile()
    _users_db[user.id] = user
    return user

def update_user(user: UserProfile) -> None:
    _users_db[user.id] = user
