# ============================================================
# EduMind AI - NSSTA / TPAC Training Service
# ============================================================

# Prototype training catalog.
# This can later be replaced with an official NSSTA/TPAC API.

TRAINING_CATALOG = [

    {
        "id": "NSSTA-001",
        "title": "Survey Design and Methodology",
        "provider": "NSSTA",
        "skill": "Survey Design",
        "level": "Intermediate",
        "duration": "5 Days",
        "description": (
            "Training on survey planning, questionnaire design, "
            "sampling concepts and survey methodology."
        ),
    },

    {
        "id": "NSSTA-002",
        "title": "Statistical Sampling Techniques",
        "provider": "NSSTA",
        "skill": "Sampling",
        "level": "Intermediate",
        "duration": "5 Days",
        "description": (
            "Training on probability sampling, sampling frames "
            "and sample selection techniques."
        ),
    },

    {
        "id": "NSSTA-003",
        "title": "Data Quality Management",
        "provider": "NSSTA",
        "skill": "Data Quality",
        "level": "Intermediate",
        "duration": "3 Days",
        "description": (
            "Training on statistical data quality, validation "
            "and quality assurance practices."
        ),
    },

    {
        "id": "NSSTA-004",
        "title": "Statistical Data Visualization",
        "provider": "NSSTA",
        "skill": "Data Visualization",
        "level": "Intermediate",
        "duration": "3 Days",
        "description": (
            "Training on presenting statistical information "
            "using effective charts and visualizations."
        ),
    },

    {
        "id": "NSSTA-005",
        "title": "Python for Statistical Analysis",
        "provider": "TPAC",
        "skill": "Python",
        "level": "Intermediate",
        "duration": "5 Days",
        "description": (
            "Practical Python training for statistical data "
            "processing and analysis."
        ),
    },

    {
        "id": "NSSTA-006",
        "title": "SQL for Statistical Data Management",
        "provider": "TPAC",
        "skill": "SQL",
        "level": "Intermediate",
        "duration": "4 Days",
        "description": (
            "Training on SQL queries, data management and "
            "database operations for statistical applications."
        ),
    },

    {
        "id": "NSSTA-007",
        "title": "Cybersecurity and Data Protection",
        "provider": "TPAC",
        "skill": "Cybersecurity",
        "level": "Intermediate",
        "duration": "3 Days",
        "description": (
            "Training on cybersecurity awareness, data "
            "protection and secure handling of information."
        ),
    },

]


# ============================================================
# GET ALL TRAININGS
# ============================================================

def get_nssta_trainings():
    """
    Return the complete NSSTA / TPAC training catalog.
    """

    return TRAINING_CATALOG


# ============================================================
# RECOMMEND TRAININGS
# ============================================================

def recommend_nssta_trainings(skill_gaps):
    """
    Match identified skill gaps with NSSTA / TPAC training.

    Supports skill-gap formats such as:

        "Python"

    or:

        {
            "skill": "Python",
            "level": "Needs Practice"
        }

    or:

        {
            "topic": "Python"
        }
    """

    recommendations = []

    if not skill_gaps:
        return recommendations


    for gap in skill_gaps:

        # ----------------------------------------------------
        # Extract skill name
        # ----------------------------------------------------

        if isinstance(gap, str):

            skill_name = gap
            gap_level = "Needs Practice"


        elif isinstance(gap, dict):

            skill_name = (
                gap.get("skill")
                or gap.get("topic")
                or gap.get("name")
                or ""
            )

            gap_level = (
                gap.get("level")
                or gap.get("gap_level")
                or "Needs Practice"
            )


        else:

            continue


        if not skill_name:
            continue


        skill_name_lower = (
            skill_name.strip().lower()
        )


        # ----------------------------------------------------
        # Find matching training
        # ----------------------------------------------------

        for training in TRAINING_CATALOG:

            training_skill_lower = (
                training["skill"]
                .strip()
                .lower()
            )


            if training_skill_lower == skill_name_lower:

                recommendation = {
                    **training,

                    "skill_gap": gap_level,

                    "reason": (
                        f"This training is recommended "
                        f"because {skill_name} was identified "
                        f"as an area requiring additional "
                        f"learning."
                    ),
                }


                recommendations.append(
                    recommendation
                )


    return recommendations