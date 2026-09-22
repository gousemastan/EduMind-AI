# ============================================================
# EduMind AI - Weak Skill Practice Service
# ============================================================

from services.quiz_service import create_quiz


def create_weak_skill_practice(
    skill_gaps,
    number_of_questions=5,
    language="English"
):
    """
    Generate personalized practice questions
    for identified weak skills.

    Reuses the existing EduMind AI quiz engine.
    """

    # --------------------------------------------------------
    # Extract weak skills
    # --------------------------------------------------------

    skills = []

    for gap in skill_gaps or []:

        if isinstance(gap, str):
            skill = gap.strip()

        elif isinstance(gap, dict):
            skill = (
                gap.get("skill")
                or gap.get("topic")
                or gap.get("name")
                or ""
            )

            skill = str(skill).strip()

        else:
            skill = ""

        if skill and skill not in skills:
            skills.append(skill)

    # --------------------------------------------------------
    # No weak skills
    # --------------------------------------------------------

    if not skills:

        return {
            "success": False,
            "skills": [],
            "number_of_questions": 0,
            "questions": [],
            "message": "No weak skills were provided."
        }

    # --------------------------------------------------------
    # Create practice source text
    # --------------------------------------------------------

    practice_text = (
        "Generate practice questions specifically "
        "for the following weak skill(s): "
        + ", ".join(skills)
        + ". Focus the questions on understanding, "
          "application, and common mistakes related "
          "to these skills."
    )

    # --------------------------------------------------------
    # Generate questions using existing quiz engine
    # --------------------------------------------------------

    try:

        questions = create_quiz(
            practice_text,
            num_questions=number_of_questions,
            language=language
        )

    except Exception as error:

        return {
            "success": False,
            "skills": skills,
            "number_of_questions": 0,
            "questions": [],
            "message": (
                "Weak-skill practice generation failed: "
                + str(error)
            )
        }

    # --------------------------------------------------------
    # Return result
    # --------------------------------------------------------

    return {
        "success": True,
        "skills": skills,
        "number_of_questions": len(questions),
        "questions": questions,
        "message": (
            "Weak-skill practice generated successfully."
        )
    }