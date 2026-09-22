# ============================================================
# EDUMIND AI
# ADAPTIVE LEARNING ROUTES
# ============================================================

from fastapi import APIRouter, Depends, Body, HTTPException

from routes.competency_routes import get_current_user_id
from services.adaptive_learning_service import (
    analyze_adaptive_learning
)


router = APIRouter(
    prefix="/api/adaptive",
    tags=["Adaptive Learning"]
)


# ============================================================
# ADAPTIVE LEARNING ANALYSIS
# ============================================================

@router.post("/analyze")
def analyze_adaptive(
    data: dict = Body(...),
    user_id: int = Depends(get_current_user_id)
):
    """
    Analyze learner performance and determine
    the next adaptive learning difficulty.
    """

    try:

        score = data.get(
            "score",
            0
        )

        total_questions = data.get(
            "total_questions",
            0
        )

        questions = data.get(
            "questions",
            []
        )

        if total_questions <= 0:

            raise HTTPException(
                status_code=400,
                detail="total_questions must be greater than 0."
            )

        if not isinstance(
            questions,
            list
        ):

            raise HTTPException(
                status_code=400,
                detail="questions must be a list."
            )

        result = analyze_adaptive_learning(
            score=score,
            total_questions=total_questions,
            questions=questions
        )

        return {
            "success": True,
            "user_id": user_id,
            "adaptive_analysis": result
        }

    except HTTPException:
        raise

    except Exception as error:

        print(
            "❌ Adaptive learning error:",
            error
        )

        raise HTTPException(
            status_code=500,
            detail="Adaptive learning analysis failed."
        )