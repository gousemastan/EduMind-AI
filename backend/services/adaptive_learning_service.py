# ============================================================
# EDUMIND AI
# ADAPTIVE LEARNING SERVICE
# ============================================================

from typing import Any


# ============================================================
# PERFORMANCE → ADAPTIVE DIFFICULTY
# ============================================================

def determine_adaptive_difficulty(
    percentage: float
) -> dict:
    """
    Determine the next learning difficulty
    from learner performance.
    """

    percentage = float(percentage)

    if percentage < 40:

        return {
            "performance": "Beginner",
            "difficulty": "Beginner",
            "action": "Strengthen fundamentals",
            "practice_mode": "Fundamental Practice",
        }

    elif percentage < 60:

        return {
            "performance": "Needs Practice",
            "difficulty": "Easy",
            "action": "Reinforce weak concepts",
            "practice_mode": "Reinforcement Practice",
        }

    elif percentage < 80:

        return {
            "performance": "Intermediate",
            "difficulty": "Intermediate",
            "action": "Continue application practice",
            "practice_mode": "Standard Practice",
        }

    else:

        return {
            "performance": "Strong",
            "difficulty": "Advanced",
            "action": "Increase challenge",
            "practice_mode": "Challenge Practice",
        }


# ============================================================
# TOPIC-LEVEL ADAPTATION
# ============================================================

def determine_topic_adaptation(
    questions: list
) -> list:
    """
    Determine adaptive difficulty separately
    for each topic.
    """

    if not questions:
        return []

    topic_stats = {}

    for question in questions:

        if not isinstance(question, dict):
            continue

        topic = str(
            question.get(
                "topic",
                "General"
            )
        ).strip()

        if not topic:
            topic = "General"

        is_correct = question.get(
            "is_correct",
            False
        )

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

        if topic not in topic_stats:

            topic_stats[topic] = {
                "total": 0,
                "correct": 0
            }

        topic_stats[topic]["total"] += 1

        if is_correct:

            topic_stats[topic]["correct"] += 1

    adaptations = []

    for topic, stats in topic_stats.items():

        total = stats["total"]
        correct = stats["correct"]

        if total <= 0:
            continue

        percentage = round(
            (correct / total) * 100,
            2
        )

        adaptive = determine_adaptive_difficulty(
            percentage
        )

        adaptations.append({

            "topic": topic,

            "score": correct,

            "total_questions": total,

            "percentage": percentage,

            "performance":
                adaptive["performance"],

            "next_difficulty":
                adaptive["difficulty"],

            "action":
                adaptive["action"],

            "practice_mode":
                adaptive["practice_mode"],

        })

    # Weakest topics first
    adaptations.sort(
        key=lambda item:
            item["percentage"]
    )

    return adaptations


# ============================================================
# COMPLETE ADAPTIVE ANALYSIS
# ============================================================

def analyze_adaptive_learning(
    score: int,
    total_questions: int,
    questions: list
) -> dict:
    """
    Perform complete adaptive-learning analysis.
    """

    if total_questions <= 0:

        return {
            "success": False,
            "score": score,
            "total_questions": total_questions,
            "percentage": 0,
            "performance": "No Data",
            "next_difficulty": "Beginner",
            "practice_mode": "Fundamental Practice",
            "topic_adaptations": [],
            "recommendation":
                "Complete a quiz to activate adaptive learning."
        }

    # --------------------------------------------------------
    # Safety
    # --------------------------------------------------------

    score = max(
        0,
        min(
            score,
            total_questions
        )
    )

    # --------------------------------------------------------
    # Overall percentage
    # --------------------------------------------------------

    percentage = round(
        (score / total_questions) * 100,
        2
    )

    # --------------------------------------------------------
    # Overall adaptation
    # --------------------------------------------------------

    adaptive = determine_adaptive_difficulty(
        percentage
    )

    # --------------------------------------------------------
    # Topic adaptation
    # --------------------------------------------------------

    topic_adaptations = determine_topic_adaptation(
        questions
    )

    # --------------------------------------------------------
    # Recommendation
    # --------------------------------------------------------

    if topic_adaptations:

        weakest_topic = topic_adaptations[0]

        recommendation = (
            f"Focus on {weakest_topic['topic']} first. "
            f"Your topic score is "
            f"{weakest_topic['percentage']}%. "
            f"Next practice should use "
            f"{weakest_topic['next_difficulty']} difficulty."
        )

    else:

        recommendation = (
            f"Your overall score is {percentage}%. "
            f"Continue with "
            f"{adaptive['practice_mode']}."
        )

    return {

        "success": True,

        "score": score,

        "total_questions":
            total_questions,

        "percentage":
            percentage,

        "performance":
            adaptive["performance"],

        "next_difficulty":
            adaptive["difficulty"],

        "action":
            adaptive["action"],

        "practice_mode":
            adaptive["practice_mode"],

        "topic_adaptations":
            topic_adaptations,

        "recommendation":
            recommendation,

    }