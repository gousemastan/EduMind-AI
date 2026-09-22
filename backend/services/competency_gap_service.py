# ============================================================
# EDUMIND AI
# COMPETENCY GAP INTELLIGENCE SERVICE
# ============================================================

from database import get_connection


# ============================================================
# COMPETENCY LEVEL SCORES
# ============================================================

LEVEL_SCORE = {
    "Beginner": 1,
    "Intermediate": 2,
    "Advanced": 3,
    "Expert": 4,
}


# ============================================================
# CALCULATE GAP
# ============================================================

def calculate_gap(current_level, target_level):

    current_score = LEVEL_SCORE.get(
        current_level,
        1
    )

    target_score = LEVEL_SCORE.get(
        target_level,
        2
    )

    difference = target_score - current_score

    if difference <= 0:
        gap_status = "No Gap"
        priority = "Low"

    elif difference == 1:
        gap_status = "Development Needed"
        priority = "Medium"

    elif difference == 2:
        gap_status = "Skill Gap"
        priority = "High"

    else:
        gap_status = "Critical Skill Gap"
        priority = "Critical"

    return {
        "current_level": current_level,
        "target_level": target_level,
        "current_score": current_score,
        "target_score": target_score,
        "gap": max(difference, 0),
        "status": gap_status,
        "priority": priority,
    }


# ============================================================
# GET USER JOB ROLE
# ============================================================

def get_user_profile(user_id):

    connection = get_connection()

    try:

        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT
                id,
                name,
                designation,
                department,
                job_role,
                education,
                experience,
                previous_training
            FROM users
            WHERE id = ?
            """,
            (user_id,)
        )

        row = cursor.fetchone()

        if not row:
            return None

        return dict(row)

    finally:

        connection.close()


# ============================================================
# GET CURRENT USER COMPETENCIES
# ============================================================

def get_user_competencies(user_id):

    connection = get_connection()

    try:

        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT
                category,
                skill,
                level,
                updated_at
            FROM user_competencies
            WHERE user_id = ?
            """,
            (user_id,)
        )

        rows = cursor.fetchall()

        competencies = {}

        for row in rows:

            category = row["category"]
            skill = row["skill"]

            if category not in competencies:
                competencies[category] = {}

            competencies[category][skill] = {
                "level": row["level"],
                "updated_at": row["updated_at"],
            }

        return competencies

    finally:

        connection.close()


# ============================================================
# GET REQUIRED FRAMEWORK
# ============================================================

def get_framework(job_role):

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

        framework = []

        for row in rows:

            framework.append(
                {
                    "category": row["category"],
                    "skill": row["skill"],
                    "target_level": row["target_level"],
                }
            )

        return framework

    finally:

        connection.close()


# ============================================================
# BUILD COMPLETE COMPETENCY GAP ANALYSIS
# ============================================================

def build_competency_gap_analysis(user_id):

    profile = get_user_profile(user_id)

    if not profile:

        return {
            "success": False,
            "message": "User profile not found.",
        }

    job_role = (
        profile.get("job_role")
        or profile.get("designation")
        or ""
    ).strip()

    if not job_role:

        return {
            "success": False,
            "message": (
                "Job role is required before "
                "competency gap analysis."
            ),
            "profile": profile,
        }

    framework = get_framework(job_role)

    if not framework:

        return {
            "success": False,
            "message": (
                f"No competency framework found "
                f"for job role: {job_role}"
            ),
            "job_role": job_role,
            "profile": profile,
        }

    current_competencies = get_user_competencies(
        user_id
    )

    gaps = []
    no_gaps = []

    category_summary = {}

    for item in framework:

        category = item["category"]
        skill = item["skill"]
        target_level = item["target_level"]

        current_data = (
            current_competencies
            .get(category, {})
            .get(skill)
        )

        if current_data:

            current_level = current_data["level"]

        else:

            current_level = "Beginner"

        comparison = calculate_gap(
            current_level=current_level,
            target_level=target_level,
        )

        result = {
            "category": category,
            "skill": skill,
            "current_level": current_level,
            "target_level": target_level,
            "current_score": comparison[
                "current_score"
            ],
            "target_score": comparison[
                "target_score"
            ],
            "gap": comparison["gap"],
            "status": comparison["status"],
            "priority": comparison["priority"],
        }

        # ----------------------------------------------------
        # Category summary
        # ----------------------------------------------------

        if category not in category_summary:

            category_summary[category] = {
                "total_skills": 0,
                "skills_with_gap": 0,
                "skills_without_gap": 0,
            }

        category_summary[category][
            "total_skills"
        ] += 1

        # ----------------------------------------------------
        # Gap classification
        # ----------------------------------------------------

        if comparison["gap"] > 0:

            gaps.append(result)

            category_summary[category][
                "skills_with_gap"
            ] += 1

        else:

            no_gaps.append(result)

            category_summary[category][
                "skills_without_gap"
            ] += 1

    # ========================================================
    # SORT GAPS
    # ========================================================

    priority_order = {
        "Critical": 1,
        "High": 2,
        "Medium": 3,
        "Low": 4,
    }

    gaps.sort(
        key=lambda item: (
            priority_order.get(
                item["priority"],
                99
            ),
            -item["gap"],
        )
    )

    # ========================================================
    # SUMMARY
    # ========================================================

    total_required = len(framework)

    total_gaps = len(gaps)

    total_completed = len(no_gaps)

    if total_required > 0:

        competency_coverage = round(
            (
                total_completed
                / total_required
            ) * 100,
            2
        )

    else:

        competency_coverage = 0

    # ========================================================
    # OVERALL STATUS
    # ========================================================

    if total_gaps == 0:

        overall_status = "Competency Target Achieved"

    elif any(
        gap["priority"] == "Critical"
        for gap in gaps
    ):

        overall_status = "Critical Skill Gaps Detected"

    elif any(
        gap["priority"] == "High"
        for gap in gaps
    ):

        overall_status = "High Priority Skill Gaps Detected"

    else:

        overall_status = "Development Areas Identified"

    # ========================================================
    # TOP RECOMMENDATIONS
    # ========================================================

    recommendations = []

    for gap in gaps[:5]:

        recommendations.append(
            {
                "skill": gap["skill"],
                "category": gap["category"],
                "priority": gap["priority"],
                "current_level": gap["current_level"],
                "target_level": gap["target_level"],
                "action": (
                    f"Develop {gap['skill']} "
                    f"from {gap['current_level']} "
                    f"towards {gap['target_level']}."
                ),
            }
        )

    # ========================================================
    # FINAL RESULT
    # ========================================================

    return {
        "success": True,

        "user_id": user_id,

        "profile": {
            "name": profile.get("name"),
            "designation": profile.get(
                "designation"
            ),
            "department": profile.get(
                "department"
            ),
            "job_role": job_role,
            "education": profile.get(
                "education"
            ),
            "experience": profile.get(
                "experience"
            ),
        },

        "summary": {
            "job_role": job_role,
            "total_required_competencies":
                total_required,
            "competencies_achieved":
                total_completed,
            "total_skill_gaps":
                total_gaps,
            "competency_coverage":
                competency_coverage,
            "overall_status":
                overall_status,
        },

        "category_summary":
            category_summary,

        "skill_gaps":
            gaps,

        "achieved_competencies":
            no_gaps,

        "recommendations":
            recommendations,
    }