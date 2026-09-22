# ============================================================
# EduMind AI - AI Revision Service
# ============================================================

from services.quiz_service import create_quiz


def create_ai_revision(
    topics,
    number_of_questions=5,
    language="English"
):
    """
    Generate a focused AI revision session
    for the learner's weak or selected topics.
    """

    skills = []

    for topic in topics or []:

        if isinstance(topic, str):
            skill = topic.strip()

        elif isinstance(topic, dict):
            skill = (
                topic.get("skill")
                or topic.get("topic")
                or topic.get("name")
                or ""
            )

            skill = str(skill).strip()

        else:
            skill = ""

        if skill and skill not in skills:
            skills.append(skill)

    if not skills:
        return {
            "success": False,
            "topics": [],
            "number_of_questions": 0,
            "questions": [],
            "message": "No revision topics were provided."
        }

    revision_text = (
        "Create a focused revision practice session "
        "for the following learning topic(s): "
        + ", ".join(skills)
        + ". Focus on the most important concepts, "
          "common mistakes, understanding, and practical "
          "application. Generate revision questions that "
          "help the learner recall and strengthen these topics."
    )

    try:

        questions = create_quiz(
            revision_text,
            num_questions=number_of_questions,
            language=language
        )

    except Exception as error:

        return {
            "success": False,
            "topics": skills,
            "number_of_questions": 0,
            "questions": [],
            "message": (
                "AI revision generation failed: "
                + str(error)
            )
        }

    return {
        "success": True,
        "topics": skills,
        "number_of_questions": len(questions),
        "questions": questions,
        "message": (
            "AI revision generated successfully."
        )
    }