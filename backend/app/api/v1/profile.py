"""
Роутер профиля пользователя.
"""

from fastapi import APIRouter, HTTPException

from app.models.profile import create_user, get_user
from app.schemas import UserProfileResponse

router = APIRouter(prefix="/api/v1/profile", tags=["profile"])


@router.post("/", response_model=UserProfileResponse)
async def create_profile():
    """Создать новый профиль пользователя."""
    user = create_user()
    return UserProfileResponse(
        user_id=user.id,
        mind_type=user.mind_type.value if user.mind_type else None,
        stress_test_completed=user.stress_test_completed,
        active_mode=user.active_mode,
    )


@router.get("/{user_id}", response_model=UserProfileResponse)
async def get_profile(user_id: str):
    """Получить профиль пользователя."""
    user = get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return UserProfileResponse(
        user_id=user.id,
        mind_type=user.mind_type.value if user.mind_type else None,
        stress_test_completed=user.stress_test_completed,
        active_mode=user.active_mode,
    )
