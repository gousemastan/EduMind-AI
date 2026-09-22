# ============================================================
# iGoT Karmayogi Course Routes
# ============================================================

from fastapi import APIRouter, Depends, Body, HTTPException
from pydantic import BaseModel
from datetime import datetime

from routes.competency_routes import get_current_user_id

from services.igot_service import (
    get_igot_courses,
    recommend_igot_courses,
)

from database import get_connection


router = APIRouter(
    prefix="/api/igot",
    tags=["iGoT Karmayogi"],
)


# ============================================================
# GET iGoT COURSES
# ============================================================

@router.get("/courses")
def get_courses(
    user_id: int = Depends(get_current_user_id),
):
    """
    Return the available iGoT course catalog.
    """

    courses = get_igot_courses()

    return {
        "success": True,
        "user_id": user_id,
        "courses": courses,
    }


# ============================================================
# iGoT COURSE RECOMMENDATIONS
# ============================================================

@router.post("/recommendations")
def get_recommendations(
    skill_gaps: list = Body(...),
    user_id: int = Depends(get_current_user_id),
):
    """
    Generate course recommendations based on skill gaps.
    """

    recommendations = recommend_igot_courses(
        skill_gaps
    )

    return {
        "success": True,
        "user_id": user_id,
        "recommendations": recommendations,
    }


# ============================================================
# iGoT COURSE ENROLLMENT
# ============================================================

class IgotEnrollmentRequest(BaseModel):
    course_id: str
    course_title: str
    skill: str = ""
    duration: str = ""


@router.post("/enroll")
def enroll_in_igot_course(
    enrollment: IgotEnrollmentRequest,
    user_id: int = Depends(get_current_user_id),
):
    """
    Enroll the authenticated user in an iGoT course.
    """

    connection = get_connection()
    cursor = connection.cursor()

    try:

        # ----------------------------------------------------
        # CHECK EXISTING ENROLLMENT
        # ----------------------------------------------------

        cursor.execute(
            """
            SELECT
                id,
                course_id,
                course_title,
                skill,
                duration,
                status,
                progress,
                enrolled_at
            FROM igot_enrollments
            WHERE user_id = ?
            AND course_id = ?
            """,
            (
                user_id,
                enrollment.course_id,
            ),
        )

        existing_enrollment = cursor.fetchone()

        if existing_enrollment:

            return {
                "success": True,
                "message": "Already enrolled in this course",
                "enrollment": {
                    "id": existing_enrollment["id"],
                    "user_id": user_id,
                    "course_id": existing_enrollment["course_id"],
                    "course_title": existing_enrollment["course_title"],
                    "skill": existing_enrollment["skill"],
                    "duration": existing_enrollment["duration"],
                    "status": existing_enrollment["status"],
                    "progress": existing_enrollment["progress"],
                    "enrolled_at": existing_enrollment["enrolled_at"],
                },
            }

        # ----------------------------------------------------
        # CREATE NEW ENROLLMENT
        # ----------------------------------------------------

        enrolled_at = datetime.utcnow().isoformat()

        cursor.execute(
            """
            INSERT INTO igot_enrollments
            (
                user_id,
                course_id,
                course_title,
                skill,
                duration,
                status,
                enrolled_at,
                progress
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                user_id,
                enrollment.course_id,
                enrollment.course_title,
                enrollment.skill,
                enrollment.duration,
                "enrolled",
                enrolled_at,
                0,
            ),
        )

        enrollment_id = cursor.lastrowid

        connection.commit()

        # ----------------------------------------------------
        # SUCCESS RESPONSE
        # ----------------------------------------------------

        return {
            "success": True,
            "message": "Course enrollment successful",
            "enrollment": {
                "id": enrollment_id,
                "user_id": user_id,
                "course_id": enrollment.course_id,
                "course_title": enrollment.course_title,
                "skill": enrollment.skill,
                "duration": enrollment.duration,
                "status": "enrolled",
                "progress": 0,
                "enrolled_at": enrolled_at,
            },
        }

    finally:

        connection.close()
        
    # ============================================================
# GET MY ENROLLED iGoT COURSES
# ============================================================

@router.get("/enrollments")
def get_my_igot_enrollments(
    user_id: int = Depends(get_current_user_id),
):
    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            SELECT
                id,
                course_id,
                course_title,
                skill,
                duration,
                status,
                progress,
                enrolled_at,
                completed_at
            FROM igot_enrollments
            WHERE user_id = ?
            ORDER BY enrolled_at DESC
            """,
            (user_id,),
        )

        rows = cursor.fetchall()

        enrollments = []

        for row in rows:
            enrollments.append({
                "id": row["id"],
                "course_id": row["course_id"],
                "course_title": row["course_title"],
                "skill": row["skill"],
                "duration": row["duration"],
                "status": row["status"],
                "progress": row["progress"],
                "enrolled_at": row["enrolled_at"],
                "completed_at": row["completed_at"],
            })

        return {
            "success": True,
            "user_id": user_id,
            "enrollments": enrollments,
        }

    finally:
        connection.close()
    
    # ============================================================
# UPDATE iGoT COURSE PROGRESS
# ============================================================

class IgotProgressRequest(BaseModel):
    enrollment_id: int
    progress: int


@router.put("/progress")
def update_igot_progress(
    progress_data: IgotProgressRequest,
    user_id: int = Depends(get_current_user_id),
):
    connection = get_connection()
    cursor = connection.cursor()

    try:
        # Check that this enrollment belongs to the logged-in user
        cursor.execute(
            """
            SELECT
                id,
                course_title,
                progress,
                status
            FROM igot_enrollments
            WHERE id = ?
            AND user_id = ?
            """,
            (
                progress_data.enrollment_id,
                user_id,
            ),
        )

        enrollment = cursor.fetchone()

        if not enrollment:
            raise HTTPException(
                status_code=404,
                detail="Enrollment not found",
            )

        # Validate progress
        if progress_data.progress < 0 or progress_data.progress > 100:
            raise HTTPException(
                status_code=400,
                detail="Progress must be between 0 and 100",
            )

        # Determine status
        if progress_data.progress == 100:
            status = "completed"
            completed_at = datetime.utcnow().isoformat()
        else:
            status = "in_progress"
            completed_at = None

        cursor.execute(
            """
            UPDATE igot_enrollments
            SET
                progress = ?,
                status = ?,
                completed_at = ?
            WHERE id = ?
            AND user_id = ?
            """,
            (
                progress_data.progress,
                status,
                completed_at,
                progress_data.enrollment_id,
                user_id,
            ),
        )

        connection.commit()

        return {
            "success": True,
            "message": "Course progress updated successfully",
            "enrollment": {
                "id": enrollment["id"],
                "course_title": enrollment["course_title"],
                "progress": progress_data.progress,
                "status": status,
                "completed_at": completed_at,
            },
        }

    finally:
        connection.close()