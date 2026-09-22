# ============================================================
# EduMind AI - Weak Skill Practice Routes
# ============================================================

from fastapi import APIRouter, Depends, Body

from routes.competency_routes import get_current_user_id

from services.weak_skill_service import (
    create_weak_skill_practice,
)

router = APIRouter(
    prefix="/api/weak-skill",
    tags=["Weak Skill Practice"],
)


@router.post("/practice")
def weak_skill_practice(
    skill_gaps: list = Body(...),
    user_id: int = Depends(get_current_user_id),
):
    practice = create_weak_skill_practice(skill_gaps)

    return {
        "success": True,
        "user_id": user_id,
        "practice": practice,
    }