# ============================================================
# EDUMIND AI
# PERSONALIZED PRACTICE SERVICE
# ============================================================

from services.quiz_service import create_quiz


# ============================================================
# GENERATE PERSONALIZED PRACTICE
# ============================================================

def generate_personalized_practice(
    topics: list,
    difficulty: str = "Intermediate",
    questions_per_topic: int = 3,
    language: str = "English"
) -> list:
    """
    Generate personalized practice questions
    for selected learner topics.

    Each topic is generated separately so that
    practice remains focused on the learner's needs.
    """

    if not topics:
        return []

    if questions_per_topic < 1:
        questions_per_topic = 1

    if questions_per_topic > 10:
        questions_per_topic = 10

    normalized_topics = []

    for topic in topics:

        if isinstance(topic, str):

            topic_name = topic.strip()

        elif isinstance(topic, dict):

            topic_name = str(
                topic.get("topic")
                or topic.get("skill")
                or topic.get("name")
                or ""
            ).strip()

        else:

            continue

        if topic_name:
            normalized_topics.append(topic_name)

    # Remove duplicate topics
    normalized_topics = list(
        dict.fromkeys(normalized_topics)
    )

    personalized_practice = []

    for topic in normalized_topics:

        # ----------------------------------------------------
        # Create focused learning material
        # ----------------------------------------------------

        practice_source = (
            f"Topic: {topic}\n\n"
            f"Generate educational practice questions "
            f"focused specifically on {topic}."
        )

        # ----------------------------------------------------
        # Generate questions using adaptive difficulty
        # ----------------------------------------------------

        questions = create_quiz(
            text=practice_source,
            num_questions=questions_per_topic,
            language=language,
            difficulty=difficulty
        )

        # ----------------------------------------------------
        # Add personalization metadata
        # ----------------------------------------------------

        for question in questions:

            question["personalized"] = True
            question["practice_topic"] = topic
            question["adaptive_difficulty"] = difficulty

        personalized_practice.extend(
            questions
        )

    return personalized_practice