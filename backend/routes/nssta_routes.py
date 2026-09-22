# ============================================================
# EduMind AI - NSSTA / TPAC Routes
# ============================================================

from fastapi import APIRouter, Depends, Body

from routes.competency_routes import get_current_user_id

from services.nssta_service import (
    get_nssta_trainings,
    recommend_nssta_trainings,
)


router = APIRouter(
    prefix="/api/nssta",
    tags=["NSSTA / TPAC Training"],
)


# ============================================================
# GET ALL NSSTA / TPAC TRAININGS
# ============================================================

@router.get("/trainings")
def get_trainings(
    user_id: int = Depends(get_current_user_id),
):
    trainings = get_nssta_trainings()

    return {
        "success": True,
        "user_id": user_id,
        "trainings": trainings,
    }


# ============================================================
# GET PERSONALIZED NSSTA / TPAC RECOMMENDATIONS
# ============================================================

@router.post("/recommendations")
def get_recommendations(
    skill_gaps: list = Body(...),
    user_id: int = Depends(get_current_user_id),
):
    recommendations = recommend_nssta_trainings(skill_gaps)

    return {
        "success": True,
        "user_id": user_id,
        "recommendations": recommendations,
    }