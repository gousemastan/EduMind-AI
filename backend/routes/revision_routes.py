# ============================================================
# EduMind AI - AI Revision Routes
# ============================================================

from fastapi import APIRouter, Depends, Body

from routes.competency_routes import get_current_user_id

from services.revision_service import (
    create_ai_revision,
)


router = APIRouter(
    prefix="/api/revision",
    tags=["AI Revision"],
)


@router.post("/practice")
def ai_revision(
    topics: list = Body(...),
    user_id: int = Depends(get_current_user_id),
):
    revision = create_ai_revision(topics)

    return {
        "success": True,
        "user_id": user_id,
        "revision": revision,
    }