from fastapi import APIRouter, Depends
from pydantic import BaseModel
import sqlite3

from database import DATABASE_PATH
from routes.auth_routes import get_current_user_id


router = APIRouter(
    prefix="/api/history",
    tags=["History"]
)


# ============================================================
# QUIZ HISTORY REQUEST MODEL
# ============================================================

class QuizHistoryRequest(BaseModel):
    quiz_title: str = "Generated Quiz"
    topic: str = "General"
    score: int = 0
    total_questions: int = 0
    percentage: float = 0
    result: str = "Completed"


# ============================================================
# GET ALL HISTORY
# ============================================================

@router.get("/")
async def get_history(
    user_id: int = Depends(get_current_user_id)
):
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # --------------------------------------------------------
    # Quiz History
    # --------------------------------------------------------

    cursor.execute(
        """
        SELECT
            id,
            quiz_title,
            topic,
            score,
            total_questions,
            percentage,
            result,
            completed_at
        FROM quiz_history
        WHERE user_id = ?
        ORDER BY completed_at DESC
        """,
        (user_id,)
    )

    quiz_history = [
        dict(row)
        for row in cursor.fetchall()
    ]

    # --------------------------------------------------------
    # Learning History
    # --------------------------------------------------------

    cursor.execute(
        """
        SELECT
            id,
            topic,
            score,
            completed,
            updated_at
        FROM learning_progress
        WHERE user_id = ?
        ORDER BY updated_at DESC
        """,
        (user_id,)
    )

    learning_history = [
        dict(row)
        for row in cursor.fetchall()
    ]

    # --------------------------------------------------------
    # Competency Assessment History
    # --------------------------------------------------------

    cursor.execute(
        """
        SELECT
            id,
            category,
            skill,
            score,
            total_questions,
            assessed_level,
            created_at
        FROM competency_assessments
        WHERE user_id = ?
        ORDER BY created_at DESC
        """,
        (user_id,)
    )

    competency_history = [
        dict(row)
        for row in cursor.fetchall()
    ]

    # --------------------------------------------------------
    # Course History
    # --------------------------------------------------------

    cursor.execute(
        """
        SELECT
            id,
            course_id,
            course_title,
            skill,
            duration,
            status,
            enrolled_at,
            completed_at,
            progress
        FROM igot_enrollments
        WHERE user_id = ?
        ORDER BY enrolled_at DESC
        """,
        (user_id,)
    )

    course_history = [
        dict(row)
        for row in cursor.fetchall()
    ]

    conn.close()

    return {
        "success": True,
        "user_id": user_id,
        "quiz_history": quiz_history,
        "learning_history": learning_history,
        "competency_history": competency_history,
        "course_history": course_history
    }


# ============================================================
# SAVE QUIZ HISTORY
# ============================================================

@router.post("/quiz")
async def save_quiz_history(
    data: QuizHistoryRequest,
    user_id: int = Depends(get_current_user_id)
):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO quiz_history (
            user_id,
            quiz_title,
            topic,
            score,
            total_questions,
            percentage,
            result
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            user_id,
            data.quiz_title,
            data.topic,
            data.score,
            data.total_questions,
            data.percentage,
            data.result
        )
    )

    conn.commit()

    history_id = cursor.lastrowid

    conn.close()

    return {
        "success": True,
        "message": "Quiz history saved successfully",
        "history_id": history_id
    }