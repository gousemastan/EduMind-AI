# ============================================================
# EDU MIND AI
# SKILL GAP DETECTION SERVICE
# ============================================================


def detect_skill_gaps(
    topics,
    score,
    total_questions,
    questions
):
    """
    Analyze quiz performance and identify
    topics that require additional practice.

    Returns:
        List of weak topics with:
        - topic
        - level
        - score_percentage
        - correct
        - incorrect
        - total
        - recommendation
    """

    # ========================================================
    # SAFETY CHECKS
    # ========================================================

    if not topics:
        return []

    if not questions:
        return []

    if total_questions <= 0:
        return []

    if score is None:
        score = 0

    # Make sure score is within valid range
    score = max(
        0,
        min(score, total_questions)
    )

    # ========================================================
    # CLEAN TOPICS
    # ========================================================

    cleaned_topics = []

    for topic in topics:

        if topic is None:
            continue

        topic_name = str(topic).strip()

        if not topic_name:
            continue

        # Avoid duplicate topics
        if topic_name.lower() not in [
            existing.lower()
            for existing in cleaned_topics
        ]:
            cleaned_topics.append(
                topic_name
            )

    if not cleaned_topics:
        return []

    # ========================================================
    # CREATE TOPIC STATISTICS
    # ========================================================

    topic_stats = {}

    for topic in cleaned_topics:

        topic_stats[topic] = {
            "correct": 0,
            "incorrect": 0,
            "total": 0
        }

    # ========================================================
    # ANALYZE QUIZ QUESTIONS
    # ========================================================

    for question in questions:

        if not isinstance(
            question,
            dict
        ):
            continue

        topic = question.get(
            "topic"
        )

        if not topic:
            continue

        topic = str(
            topic
        ).strip()

        if not topic:
            continue

        # ----------------------------------------------------
        # Find matching topic
        # ----------------------------------------------------

        matching_topic = None

        for existing_topic in topic_stats:

            if (
                existing_topic.lower()
                == topic.lower()
            ):

                matching_topic = (
                    existing_topic
                )

                break

        # ----------------------------------------------------
        # If topic wasn't detected originally,
        # add it dynamically
        # ----------------------------------------------------

        if matching_topic is None:

            topic_stats[topic] = {
                "correct": 0,
                "incorrect": 0,
                "total": 0
            }

            matching_topic = topic

        # ----------------------------------------------------
        # Count question
        # ----------------------------------------------------

        topic_stats[
            matching_topic
        ]["total"] += 1

        # ----------------------------------------------------
        # Check answer
        # ----------------------------------------------------

        is_correct = question.get(
            "is_correct",
            False
        )

        # Handle string values safely
        if isinstance(
            is_correct,
            str
        ):

            is_correct = (
                is_correct.lower()
                in [
                    "true",
                    "1",
                    "yes"
                ]
            )

        if is_correct:

            topic_stats[
                matching_topic
            ]["correct"] += 1

        else:

            topic_stats[
                matching_topic
            ]["incorrect"] += 1

    # ========================================================
    # CALCULATE OVERALL PERFORMANCE
    # ========================================================

    overall_percentage = (
        score / total_questions
    ) * 100

    # ========================================================
    # CREATE SKILL GAPS
    # ========================================================

    skill_gaps = []

    for topic in cleaned_topics:

        stats = topic_stats.get(
            topic,
            {
                "correct": 0,
                "incorrect": 0,
                "total": 0
            }
        )

        correct = stats[
            "correct"
        ]

        incorrect = stats[
            "incorrect"
        ]

        total = stats[
            "total"
        ]

        # ----------------------------------------------------
        # Calculate topic percentage
        # ----------------------------------------------------

        if total > 0:

            topic_percentage = (
                correct / total
            ) * 100

        else:

            # No question directly mapped
            # to this topic.
            topic_percentage = (
                overall_percentage
            )

        # ----------------------------------------------------
        # Determine skill level
        # ----------------------------------------------------

        if topic_percentage < 40:

            level = "Beginner"

            recommendation = (
                "This topic needs significant "
                "practice. Review the fundamentals "
                "and solve basic questions before "
                "moving to advanced concepts."
            )

        elif topic_percentage < 60:

            level = "Needs Practice"

            recommendation = (
                "Review the important concepts "
                "in this topic and practice "
                "additional questions."
            )

        elif topic_percentage < 80:

            level = "Intermediate"

            recommendation = (
                "You have a reasonable understanding "
                "of this topic. Practice more "
                "application-based questions to "
                "strengthen your knowledge."
            )

        else:

            level = "Strong"

            recommendation = (
                "You are performing well in this "
                "topic. Continue practicing to "
                "maintain your knowledge."
            )

        # ====================================================
        # ONLY ADD WEAK AREAS
        # ====================================================

        if topic_percentage < 80:

            skill_gaps.append({

                "topic": topic,

                "level": level,

                "score_percentage": round(
                    topic_percentage,
                    2
                ),

                "correct": correct,

                "incorrect": incorrect,

                "total": total,

                "recommendation":
                    recommendation
            })

    # ========================================================
    # NO SKILL GAPS
    # ========================================================

    if not skill_gaps:

        return []

    # ========================================================
    # SORT BY WEAKEST TOPIC
    # ========================================================

    skill_gaps.sort(
        key=lambda item:
            item["score_percentage"]
    )

    # ========================================================
    # RETURN RESULT
    # ========================================================

    return skill_gaps