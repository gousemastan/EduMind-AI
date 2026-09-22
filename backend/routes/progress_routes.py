from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from database import get_connection
from auth_utils import get_current_user_id


router = APIRouter(
    prefix="/api/progress",
    tags=["Learning Progress"]
)


class ProgressRequest(BaseModel):
    topic: str
    score: int
    total_questions: int
    completed: bool = True


@router.post("/save")
def save_progress(
    data: ProgressRequest,
    user_id: int = Depends(get_current_user_id)
):

    topic = data.topic.strip()

    if not topic:
        raise HTTPException(
            status_code=400,
            detail="Topic is required."
        )

    if data.total_questions <= 0:
        raise HTTPException(
            status_code=400,
            detail="Total questions must be greater than 0."
        )

    if data.score < 0 or data.score > data.total_questions:
        raise HTTPException(
            status_code=400,
            detail="Invalid score."
        )

    connection = get_connection()

    try:

        cursor = connection.cursor()

        # Check whether this user already has progress for this topic
        cursor.execute(
            """
            SELECT id
            FROM learning_progress
            WHERE user_id = ?
            AND topic = ?
            """,
            (user_id, topic)
        )

        existing_progress = cursor.fetchone()

        # Use the same database timestamp format
        cursor.execute(
            "SELECT datetime('now') AS current_time"
        )

        current_time = cursor.fetchone()["current_time"]

        if existing_progress:

            # Update existing progress
            cursor.execute(
                """
                UPDATE learning_progress
                SET score = ?,
                    completed = ?,
                    updated_at = ?
                WHERE user_id = ?
                AND topic = ?
                """,
                (
                    data.score,
                    int(data.completed),
                    current_time,
                    user_id,
                    topic
                )
            )

        else:

            # Create new progress
            cursor.execute(
                """
                INSERT INTO learning_progress
                (
                    user_id,
                    topic,
                    score,
                    completed,
                    updated_at
                )
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    user_id,
                    topic,
                    data.score,
                    int(data.completed),
                    current_time
                )
            )

        connection.commit()

        percentage = round(
            (data.score / data.total_questions) * 100,
            2
        )

        return {
            "success": True,
            "message": "Learning progress saved successfully.",
            "progress": {
                "topic": topic,
                "score": data.score,
                "total_questions": data.total_questions,
                "percentage": percentage,
                "completed": data.completed
            }
        }

    finally:

        connection.close()


@router.get("/")
def get_progress(
    user_id: int = Depends(get_current_user_id)
):

    connection = get_connection()

    try:

        cursor = connection.cursor()

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

        rows = cursor.fetchall()

        progress = []

        for row in rows:

            progress.append(
                {
                    "id": row["id"],
                    "topic": row["topic"],
                    "score": row["score"],
                    "completed": bool(row["completed"]),
                    "updated_at": row["updated_at"]
                }
            )

        return {
            "success": True,
            "progress": progress
        }

    finally:

        connection.close()