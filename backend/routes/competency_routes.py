import os

import jwt
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException
from services.competency_assessment_service import (
    generate_competency_assessment,
    evaluate_competency_assessment,
)

from services.competency_gap_service import (
    build_competency_gap_analysis
)

from services.learning_path_service import (
    create_competency_learning_path
)
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel

from database import get_connection


load_dotenv()


# ============================================================
# ROUTER
# ============================================================

router = APIRouter(
    prefix="/api/competencies",
    tags=["Competencies"]
)


security = HTTPBearer()


# ============================================================
# JWT CONFIGURATION
# ============================================================

JWT_SECRET_KEY = os.getenv(
    "JWT_SECRET_KEY",
    "edumind-development-secret-change-this"
)

JWT_ALGORITHM = "HS256"


# ============================================================
# VALID COMPETENCY LEVELS
# ============================================================

VALID_LEVELS = {
    "Beginner",
    "Intermediate",
    "Advanced",
    "Expert"
}


# ============================================================
# VALID COMPETENCIES
# ============================================================

VALID_COMPETENCIES = {

    "Statistical": [
        "Survey Design",
        "Sampling",
        "National Accounts",
        "Price Statistics",
        "Labour Statistics",
        "Agricultural Statistics",
        "Industrial Statistics",
        "SDG Indicators",
        "Data Quality",
    ],

    "Technical": [
        "Python",
        "R",
        "SQL",
        "Stata",
        "SPSS",
        "SAS",
        "GIS",
        "Data Visualization",
        "AI / ML",
        "Cloud Computing",
        "APIs",
    ],

    "Digital Governance": [
        "Cybersecurity",
        "Data Privacy",
        "Digital Signatures",
        "Government Cloud",
        "Digital Public Infrastructure",
    ],

    "Behavioural / Managerial": [
        "Leadership",
        "Communication",
        "Project Management",
        "Ethics",
        "Decision Making",
        "Change Management",
    ],
}


# ============================================================
# REQUEST MODELS
# ============================================================

class CompetencyRequest(BaseModel):
    category: str
    skill: str
    level: str


class CompetencyBulkRequest(BaseModel):
    competencies: dict[str, dict[str, str]]
    

class AssessmentGenerateRequest(BaseModel):
    category: str
    skill: str
    current_level: str = "Beginner"
    target_level: str = "Intermediate"


class AssessmentSubmitRequest(BaseModel):
    category: str
    skill: str
    questions: list
    answers: list


# ============================================================
# GET CURRENT USER FROM JWT
# ============================================================

def get_current_user_id(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials

    try:

        payload = jwt.decode(
            token,
            JWT_SECRET_KEY,
            algorithms=[JWT_ALGORITHM]
        )

        user_id = payload.get("sub")

        if not user_id:
            raise HTTPException(
                status_code=401,
                detail="Invalid authentication token"
            )

        return int(user_id)

    except (jwt.InvalidTokenError, ValueError):

        raise HTTPException(
            status_code=401,
            detail="Invalid or expired authentication token"
        )


# ============================================================
# VALIDATE COMPETENCY
# ============================================================

def validate_competency(
    category: str,
    skill: str,
    level: str
):

    # Check category
    if category not in VALID_COMPETENCIES:

        raise HTTPException(
            status_code=400,
            detail="Invalid competency category"
        )

    # Check skill
    if skill not in VALID_COMPETENCIES[category]:

        raise HTTPException(
            status_code=400,
            detail="Invalid competency skill"
        )

    # Check level
    if level not in VALID_LEVELS:

        raise HTTPException(
            status_code=400,
            detail="Invalid competency level"
        )


# ============================================================
# GET USER COMPETENCY PROFILE
# ============================================================

@router.get("")
def get_competencies(
    user_id: int = Depends(get_current_user_id)
):

    connection = get_connection()

    try:

        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT
                category,
                skill,
                level
            FROM user_competencies
            WHERE user_id = ?
            ORDER BY category, skill
            """,
            (user_id,)
        )

        rows = cursor.fetchall()

        competencies = {}

        for row in rows:

            category = row["category"]
            skill = row["skill"]
            level = row["level"]

            if category not in competencies:
                competencies[category] = {}

            competencies[category][skill] = level

        return {
            "message": "Competencies retrieved successfully",
            "competencies": competencies
        }

    finally:

        connection.close()


# ============================================================
# UPDATE ONE COMPETENCY
# ============================================================

@router.put("")
def update_competency(
    data: CompetencyRequest,
    user_id: int = Depends(get_current_user_id)
):

    # Validate input
    validate_competency(
        data.category,
        data.skill,
        data.level
    )

    connection = get_connection()

    try:

        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO user_competencies
            (
                user_id,
                category,
                skill,
                level
            )
            VALUES (?, ?, ?, ?)

            ON CONFLICT(user_id, category, skill)
            DO UPDATE SET
                level = excluded.level,
                updated_at = CURRENT_TIMESTAMP
            """,
            (
                user_id,
                data.category,
                data.skill,
                data.level
            )
        )

        connection.commit()

        return {
            "message": "Competency updated successfully",

            "competency": {
                "category": data.category,
                "skill": data.skill,
                "level": data.level
            }
        }

    finally:

        connection.close()


# ============================================================
# SAVE ALL COMPETENCIES
# ============================================================

@router.post("")
def save_all_competencies(
    data: CompetencyBulkRequest,
    user_id: int = Depends(get_current_user_id)
):

    connection = get_connection()

    try:

        cursor = connection.cursor()

        saved_count = 0

        for category, skills in data.competencies.items():

            for skill, level in skills.items():

                # Validate each competency
                validate_competency(
                    category,
                    skill,
                    level
                )

                cursor.execute(
                    """
                    INSERT INTO user_competencies
                    (
                        user_id,
                        category,
                        skill,
                        level
                    )
                    VALUES (?, ?, ?, ?)

                    ON CONFLICT(user_id, category, skill)
                    DO UPDATE SET
                        level = excluded.level,
                        updated_at = CURRENT_TIMESTAMP
                    """,
                    (
                        user_id,
                        category,
                        skill,
                        level
                    )
                )

                saved_count += 1

        connection.commit()

        return {
            "message": "Competency profile saved successfully",
            "saved_count": saved_count
        }

    finally:

        connection.close()


# ============================================================
# GET COMPETENCY FRAMEWORK FOR JOB ROLE
# ============================================================

@router.get("/framework/{job_role}")
def get_competency_framework(
    job_role: str,
    user_id: int = Depends(get_current_user_id)
):

    connection = get_connection()

    try:

        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT
                category,
                skill,
                target_level
            FROM competency_framework
            WHERE job_role = ?
            ORDER BY category, skill
            """,
            (job_role,)
        )

        rows = cursor.fetchall()

        framework = {}

        for row in rows:

            category = row["category"]
            skill = row["skill"]
            target_level = row["target_level"]

            if category not in framework:
                framework[category] = {}

            framework[category][skill] = target_level

        return {
            "job_role": job_role,
            "framework": framework
        }

    finally:

        connection.close()
        
@router.post("/assessment/generate")
def generate_assessment(
    request: AssessmentGenerateRequest,
    user_id: int = Depends(get_current_user_id),
):
    try:
        assessment = generate_competency_assessment(
            category=request.category,
            skill=request.skill,
            current_level=request.current_level,
            target_level=request.target_level,
        )

        return {
            "success": True,
            "user_id": user_id,
            "assessment": assessment,
        }

    except Exception as error:
        print("❌ Competency assessment generation error:", error)

        raise HTTPException(
            status_code=500,
            detail=str(error),
        )
@router.post("/assessment/submit")
def submit_assessment(
    request: AssessmentSubmitRequest,
    user_id: int = Depends(get_current_user_id),
):
    try:
        result = evaluate_competency_assessment(
            category=request.category,
            skill=request.skill,
            questions=request.questions,
            answers=request.answers,
        )

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO competency_assessments
            (
                user_id,
                category,
                skill,
                score,
                total_questions,
                assessed_level
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                user_id,
                result["category"],
                result["skill"],
                result["score"],
                result["total_questions"],
                result["assessed_level"],
            ),
        )

            # ========================================================
        # UPDATE USER COMPETENCY PROFILE
        # ========================================================

        cursor.execute(
            """
            INSERT INTO user_competencies
            (
                user_id,
                category,
                skill,
                level
            )
            VALUES (?, ?, ?, ?)

            ON CONFLICT(user_id, category, skill)
            DO UPDATE SET
                level = excluded.level,
                updated_at = CURRENT_TIMESTAMP
            """,
            (
                user_id,
                result["category"],
                result["skill"],
                result["assessed_level"],
            ),
        )

        connection.commit()
        connection.close()

        return {
            "success": True,
            "user_id": user_id,
            "result": result,
            "competency_updated": True,
        }

    except Exception as error:
        print("❌ Competency assessment submission error:", error)

        raise HTTPException(
            status_code=500,
            detail=str(error),
        )
        
        # ============================================================
# COMPLETE AI COMPETENCY GAP ANALYSIS
# ============================================================

@router.get("/gap-analysis")
def get_competency_gap_analysis(
    user_id: int = Depends(get_current_user_id),
):

    try:

        result = build_competency_gap_analysis(
            user_id
        )

        if not result.get("success"):

            raise HTTPException(
                status_code=400,
                detail=result.get(
                    "message",
                    "Competency gap analysis failed."
                ),
            )

        return result

    except HTTPException:

        raise

    except Exception as error:

        print(
            "❌ Competency gap analysis error:",
            error
        )

        raise HTTPException(
            status_code=500,
            detail=(
                "Unable to calculate competency "
                "gap analysis."
            ),
        )
        
        
        
@router.post("/personalized-learning-path")
async def get_personalized_learning_path(
    user_id: int = Depends(get_current_user_id)
):
    """
    Generate a personalized learning path
    based on the user's competency gaps.
    """

    gap_analysis = build_competency_gap_analysis(user_id)

    learning_path = create_competency_learning_path(
        gap_analysis
    )

    return {
        "success": True,
        "user_id": user_id,
        "learning_path": learning_path
    }