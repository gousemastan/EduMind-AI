# ============================================================
# EDUMIND AI
# ADMIN DASHBOARD ROUTES
# ============================================================

from fastapi import APIRouter, Depends, HTTPException

from auth_utils import get_current_user_id
from database import get_connection


router = APIRouter(
    prefix="/api/admin",
    tags=["Administrator Dashboard"]
)


# ============================================================
# ADMIN ROLE CHECK
# ============================================================

def get_admin_user_id(
    user_id: int = Depends(get_current_user_id)
):
    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT id, name, email, role
            FROM users
            WHERE id = ?
            """,
            (user_id,)
        )

        user = cursor.fetchone()

    finally:
        connection.close()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found."
        )

    role = str(
        user["role"] or ""
    ).strip().lower()

    if role != "admin":
        raise HTTPException(
            status_code=403,
            detail="Administrator access required."
        )

    return user["id"]


# ============================================================
# ADMIN DASHBOARD
#
# GET /api/admin/dashboard
# ============================================================

@router.get("/dashboard")
async def admin_dashboard(
    admin_user_id: int = Depends(get_admin_user_id)
):

    connection = get_connection()

    try:

        cursor = connection.cursor()

        # ====================================================
        # 1. TOTAL USERS
        # ====================================================

        cursor.execute(
            """
            SELECT COUNT(*) AS total_users
            FROM users
            """
        )

        row = cursor.fetchone()

        total_users = (
            int(row["total_users"])
            if row
            else 0
        )

        # ====================================================
        # 2. TOTAL ADMINS
        # ====================================================

        cursor.execute(
            """
            SELECT COUNT(*) AS total_admins
            FROM users
            WHERE LOWER(TRIM(role)) = 'admin'
            """
        )

        row = cursor.fetchone()

        total_admins = (
            int(row["total_admins"])
            if row
            else 0
        )

        # ====================================================
        # 3. TOTAL LEARNERS
        # ====================================================

        cursor.execute(
            """
            SELECT COUNT(*) AS total_learners
            FROM users
            WHERE LOWER(
                TRIM(
                    COALESCE(role, 'learner')
                )
            ) != 'admin'
            """
        )

        row = cursor.fetchone()

        total_learners = (
            int(row["total_learners"])
            if row
            else 0
        )

        # ====================================================
        # 4. ACTIVE LEARNERS
        #
        # Learner with at least one learning_progress record.
        # ====================================================

        cursor.execute(
            """
            SELECT COUNT(DISTINCT lp.user_id)
                   AS active_learners

            FROM learning_progress lp

            INNER JOIN users u
                ON u.id = lp.user_id

            WHERE LOWER(
                TRIM(
                    COALESCE(u.role, 'learner')
                )
            ) != 'admin'
            """
        )

        row = cursor.fetchone()

        active_learners = (
            int(row["active_learners"])
            if row
            else 0
        )

        # ====================================================
        # 5. AVERAGE PROGRESS
        # ====================================================

        cursor.execute(
            """
            SELECT AVG(lp.score)
                   AS average_progress

            FROM learning_progress lp

            INNER JOIN users u
                ON u.id = lp.user_id

            WHERE LOWER(
                TRIM(
                    COALESCE(u.role, 'learner')
                )
            ) != 'admin'
            """
        )

        row = cursor.fetchone()

        average_progress = (
            round(
                float(row["average_progress"]),
                2
            )
            if row
            and row["average_progress"] is not None
            else 0
        )

        # ====================================================
        # 6. COMPETENCY OVERVIEW
        #
        # Shows:
        # - Category
        # - Skill
        # - Number of learners assessed
        # - Average assessment percentage
        # ====================================================

        cursor.execute(
            """
            SELECT
                ca.category,
                ca.skill,

                COUNT(
                    DISTINCT ca.user_id
                ) AS learner_count,

                ROUND(
                    AVG(
                        CASE
                            WHEN ca.total_questions > 0
                            THEN
                                (
                                    CAST(
                                        ca.score AS REAL
                                    )
                                    / ca.total_questions
                                ) * 100
                            ELSE 0
                        END
                    ),
                    2
                ) AS average_score

            FROM competency_assessments ca

            INNER JOIN users u
                ON u.id = ca.user_id

            WHERE LOWER(
                TRIM(
                    COALESCE(
                        u.role,
                        'learner'
                    )
                )
            ) != 'admin'

            GROUP BY
                ca.category,
                ca.skill

            ORDER BY
                ca.category,
                ca.skill
            """
        )

        competency_overview = []

        for row in cursor.fetchall():

            competency_overview.append(
                {
                    "category": row["category"],

                    "skill": row["skill"],

                    "learner_count": int(
                        row["learner_count"] or 0
                    ),

                    "average_score": float(
                        row["average_score"] or 0
                    )
                }
            )

        # ====================================================
        # 7. COMPETENCY DISTRIBUTION
        #
        # Beginner / Intermediate / Advanced / Expert
        # ====================================================

        cursor.execute(
            """
            SELECT
                level,
                COUNT(*) AS count

            FROM user_competencies uc

            INNER JOIN users u
                ON u.id = uc.user_id

            WHERE LOWER(
                TRIM(
                    COALESCE(
                        u.role,
                        'learner'
                    )
                )
            ) != 'admin'

            GROUP BY level

            ORDER BY level
            """
        )

        competency_distribution = []

        for row in cursor.fetchall():

            competency_distribution.append(
                {
                    "level": row["level"],

                    "count": int(
                        row["count"] or 0
                    )
                }
            )

        # ====================================================
        # 8. TRAINING ACTIVITY
        #
        # Uses learning_progress records.
        # ====================================================

        cursor.execute(
            """
            SELECT
                lp.topic,

                COUNT(*) AS activity_count,

                COUNT(
                    CASE
                        WHEN lp.completed = 1
                        THEN 1
                    END
                ) AS completed_count,

                ROUND(
                    AVG(lp.score),
                    2
                ) AS average_score

            FROM learning_progress lp

            INNER JOIN users u
                ON u.id = lp.user_id

            WHERE LOWER(
                TRIM(
                    COALESCE(
                        u.role,
                        'learner'
                    )
                )
            ) != 'admin'

            GROUP BY lp.topic

            ORDER BY activity_count DESC
            """
        )

        training_activity = []

        for row in cursor.fetchall():

            training_activity.append(
                {
                    "topic": row["topic"],

                    "activity_count": int(
                        row["activity_count"] or 0
                    ),

                    "completed_count": int(
                        row["completed_count"] or 0
                    ),

                    "average_score": float(
                        row["average_score"] or 0
                    )
                }
            )

        # ====================================================
        # 9. TRAINING EFFECTIVENESS
        #
        # Uses competency assessment performance.
        #
        # Effectiveness score =
        # average assessment percentage.
        # ====================================================

        cursor.execute(
            """
            SELECT
                ca.skill,

                COUNT(*) AS assessment_count,

                ROUND(
                    AVG(
                        CASE
                            WHEN ca.total_questions > 0
                            THEN
                                (
                                    CAST(
                                        ca.score AS REAL
                                    )
                                    / ca.total_questions
                                ) * 100
                            ELSE 0
                        END
                    ),
                    2
                ) AS effectiveness_score

            FROM competency_assessments ca

            INNER JOIN users u
                ON u.id = ca.user_id

            WHERE LOWER(
                TRIM(
                    COALESCE(
                        u.role,
                        'learner'
                    )
                )
            ) != 'admin'

            GROUP BY ca.skill

            ORDER BY effectiveness_score DESC
            """
        )

        training_effectiveness = []

        for row in cursor.fetchall():

            training_effectiveness.append(
                {
                    "skill": row["skill"],

                    "assessment_count": int(
                        row["assessment_count"] or 0
                    ),

                    "effectiveness_score": float(
                        row["effectiveness_score"] or 0
                    )
                }
            )

        # ====================================================
        # 10. LEARNING HOURS
        #
        # Calculates earned learning hours from iGoT courses.
        #
        # Example:
        # 5 hours × 100% = 5 hours
        # 5 hours × 50%  = 2.5 hours
        # ====================================================

        cursor.execute(
            """
            SELECT
                duration,
                progress

            FROM igot_enrollments ie

            INNER JOIN users u
                ON u.id = ie.user_id

            WHERE LOWER(
                TRIM(
                    COALESCE(
                        u.role,
                        'learner'
                    )
                )
            ) != 'admin'
            """
        )

        total_learning_hours = 0.0

        for row in cursor.fetchall():

            duration_text = str(
                row["duration"] or ""
            ).strip()

            try:

                progress = float(
                    row["progress"] or 0
                )

                hours_text = (
                    duration_text
                    .lower()
                    .replace("hours", "")
                    .replace("hour", "")
                    .strip()
                )

                course_hours = float(
                    hours_text
                )

                earned_hours = (
                    course_hours
                    * progress
                    / 100
                )

                total_learning_hours += (
                    earned_hours
                )

            except (
                ValueError,
                TypeError
            ):

                continue

        total_learning_hours = round(
            total_learning_hours,
            2
        )

        # ====================================================
        # 11. EMERGING SKILLS
        #
        # Identifies skills appearing in learner competency
        # records.
        #
        # These are data-driven indicators from the current
        # platform data, not external labor-market forecasts.
        # ====================================================

        cursor.execute(
            """
            SELECT
                skill,
                COUNT(*) AS learner_count

            FROM user_competencies uc

            INNER JOIN users u
                ON u.id = uc.user_id

            WHERE LOWER(
                TRIM(
                    COALESCE(
                        u.role,
                        'learner'
                    )
                )
            ) != 'admin'

            GROUP BY skill

            ORDER BY
                learner_count DESC,
                skill

            LIMIT 10
            """
        )

        emerging_skills = []

        for row in cursor.fetchall():

            emerging_skills.append(
                {
                    "skill": row["skill"],

                    "learner_count": int(
                        row["learner_count"] or 0
                    )
                }
            )

        # ====================================================
        # 12. PREDICTIVE SKILL REQUIREMENTS
        #
        # Compares:
        #
        #   Learner current competency
        #                VS
        #   Required competency framework level
        #
        # A skill is included when:
        #
        #   1. The learner has no competency record
        #      OR
        #
        #   2. Current level is below target level.
        #
        # This is a rule-based skill-gap projection using
        # current platform data.
        #
        # It is NOT an external labor-market forecast.
        # ====================================================

        level_scores = {
            "beginner": 1,
            "intermediate": 2,
            "advanced": 3,
            "expert": 4
        }

        cursor.execute(
            """
            SELECT
                u.id AS user_id,
                u.job_role,

                cf.category,
                cf.skill,
                cf.target_level,

                uc.level AS current_level

            FROM users u

            INNER JOIN competency_framework cf
                ON LOWER(
                    TRIM(
                        COALESCE(
                            u.job_role,
                            ''
                        )
                    )
                )
                =
                LOWER(
                    TRIM(
                        COALESCE(
                            cf.job_role,
                            ''
                        )
                    )
                )

            LEFT JOIN user_competencies uc
                ON uc.user_id = u.id

                AND LOWER(
                    TRIM(
                        COALESCE(
                            uc.category,
                            ''
                        )
                    )
                )
                =
                LOWER(
                    TRIM(
                        COALESCE(
                            cf.category,
                            ''
                        )
                    )
                )

                AND LOWER(
                    TRIM(
                        COALESCE(
                            uc.skill,
                            ''
                        )
                    )
                )
                =
                LOWER(
                    TRIM(
                        COALESCE(
                            cf.skill,
                            ''
                        )
                    )
                )

            WHERE LOWER(
                TRIM(
                    COALESCE(
                        u.role,
                        'learner'
                    )
                )
            ) != 'admin'

            AND TRIM(
                COALESCE(
                    u.job_role,
                    ''
                )
            ) != ''
            """
        )

        predictive_skill_map = {}

        for row in cursor.fetchall():

            target_level = str(
                row["target_level"] or ""
            ).strip()

            current_level = str(
                row["current_level"] or ""
            ).strip()

            target_score = level_scores.get(
                target_level.lower(),
                0
            )

            current_score = level_scores.get(
                current_level.lower(),
                0
            )

            # ------------------------------------------------
            # Missing skill OR below target level
            # ------------------------------------------------

            if current_score < target_score:

                skill = str(
                    row["skill"] or ""
                ).strip()

                category = str(
                    row["category"] or ""
                ).strip()

                if not skill:
                    continue

                key = (
                    category.lower(),
                    skill.lower(),
                    target_level.lower()
                )

                if key not in predictive_skill_map:

                    predictive_skill_map[key] = {
                        "skill": skill,
                        "category": category,
                        "target_level": target_level,
                        "learner_count": 0
                    }

                predictive_skill_map[key][
                    "learner_count"
                ] += 1

        predictive_skill_requirements = list(
            predictive_skill_map.values()
        )

        # ----------------------------------------------------
        # Sort:
        # Most affected learners first
        # ----------------------------------------------------

        predictive_skill_requirements.sort(
            key=lambda item: (
                -item["learner_count"],
                item["category"],
                item["skill"]
            )
        )

        # ----------------------------------------------------
        # Show maximum 10 skills
        # ----------------------------------------------------

        predictive_skill_requirements = (
            predictive_skill_requirements[:10]
        )

    finally:

        connection.close()

    # ========================================================
    # FINAL RESPONSE
    # ========================================================

    return {

        "success": True,

        "message":
            "Administrator dashboard data retrieved successfully.",

        "admin_user_id":
            admin_user_id,

        "dashboard": {

            "total_users":
                total_users,

            "total_learners":
                total_learners,

            "total_admins":
                total_admins,

            "active_learners":
                active_learners,

            "average_progress":
                average_progress,

            "total_learning_hours":
                total_learning_hours,

            "competency_overview":
                competency_overview,

            "competency_distribution":
                competency_distribution,

            "training_activity":
                training_activity,

            "training_effectiveness":
                training_effectiveness,

            "emerging_skills":
                emerging_skills,

            "predictive_skill_requirements":
                predictive_skill_requirements
        }
    }