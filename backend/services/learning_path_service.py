# ============================================================
# EDU MIND AI
# PERSONALIZED LEARNING PATH SERVICE
# ============================================================


# ============================================================
# QUIZ RESULT ANALYSIS
# ============================================================

def analyze_quiz_results(
    score,
    total_questions,
    questions
):
    """
    Analyze quiz results and create a personalized
    learning path based on the user's performance.
    """

    # ========================================================
    # SAFETY CHECKS
    # ========================================================

    if total_questions <= 0:
        return {
            "score": score,
            "total_questions": total_questions,
            "percentage": 0,
            "performance": "No Data",
            "weak_topics": [],
            "strong_topics": [],
            "learning_path": [],
            "learning_order": [],
            "recommendation": (
                "Complete the quiz to generate a learning path."
            ),
            "overall_recommendation": (
                "Complete the quiz to generate a learning path."
            )
        }

    if score < 0:
        score = 0

    if score > total_questions:
        score = total_questions

    # ========================================================
    # CALCULATE PERCENTAGE
    # ========================================================

    percentage = round(
        (score / total_questions) * 100,
        2
    )

    # ========================================================
    # DETERMINE OVERALL PERFORMANCE
    # ========================================================

    if percentage < 40:

        performance = "Beginner"

        overall_recommendation = (
            "You need to strengthen the fundamentals. "
            "Start with basic concepts before moving to "
            "advanced topics."
        )

    elif percentage < 60:

        performance = "Needs Practice"

        overall_recommendation = (
            "You have some understanding of the material, "
            "but several concepts need additional practice."
        )

    elif percentage < 80:

        performance = "Intermediate"

        overall_recommendation = (
            "You have a good foundation. Focus on weak topics "
            "and practice application-based questions."
        )

    else:

        performance = "Strong"

        overall_recommendation = (
            "Excellent performance. Continue practicing and "
            "challenge yourself with advanced concepts."
        )

    # ========================================================
    # TOPIC STATISTICS
    # ========================================================

    topic_stats = {}

    for question in questions or []:

        topic = question.get(
            "topic",
            "General"
        )

        topic = str(
            topic or "General"
        ).strip()

        if not topic:
            topic = "General"

        if topic not in topic_stats:

            topic_stats[topic] = {
                "correct": 0,
                "incorrect": 0,
                "total": 0
            }

        topic_stats[topic]["total"] += 1

        is_correct = question.get(
            "is_correct",
            False
        )

        if is_correct:
            topic_stats[topic]["correct"] += 1
        else:
            topic_stats[topic]["incorrect"] += 1

    # ========================================================
    # WEAK AND STRONG TOPICS
    # ========================================================

    weak_topics = []
    strong_topics = []

    for topic, stats in topic_stats.items():

        total = stats["total"]
        correct = stats["correct"]

        if total <= 0:
            continue

        topic_percentage = round(
            (correct / total) * 100,
            2
        )

        if topic_percentage < 60:

            weak_topics.append({
                "topic": topic,
                "percentage": topic_percentage,
                "correct": correct,
                "incorrect": stats["incorrect"],
                "total": total
            })

        elif topic_percentage >= 80:

            strong_topics.append({
                "topic": topic,
                "percentage": topic_percentage,
                "correct": correct,
                "incorrect": stats["incorrect"],
                "total": total
            })

    # ========================================================
    # SORT TOPICS
    # ========================================================

    weak_topics.sort(
        key=lambda item: item["percentage"]
    )

    strong_topics.sort(
        key=lambda item: item["percentage"],
        reverse=True
    )

    # ========================================================
    # CREATE LEARNING PATH
    # ========================================================

    learning_path = []

    # ========================================================
    # ADD WEAK TOPICS FIRST
    # ========================================================

    for index, topic_data in enumerate(
        weak_topics,
        start=1
    ):

        topic = topic_data["topic"]
        topic_percentage = topic_data["percentage"]

        # ----------------------------------------------------
        # DETERMINE LEVEL
        # ----------------------------------------------------

        if topic_percentage < 40:

            level = "Beginner"
            estimated_time = "2-3 hours"

            study_topics = [
                f"Understand the fundamentals of {topic}",
                f"Learn the important concepts of {topic}",
                f"Study basic examples of {topic}",
                f"Practice simple problems related to {topic}"
            ]

            practice = [
                "10 basic questions",
                "5 concept-based questions",
                "Review incorrect answers"
            ]

        else:

            level = "Needs Practice"
            estimated_time = "1-2 hours"

            study_topics = [
                f"Review the important concepts of {topic}",
                f"Study examples related to {topic}",
                f"Identify common mistakes in {topic}",
                f"Practice application-based questions"
            ]

            practice = [
                "10 practice questions",
                "5 application-based questions",
                "Review incorrect answers"
            ]

        # ----------------------------------------------------
        # ADD LEARNING PATH ITEM
        # ----------------------------------------------------

        learning_path.append({
            "priority": index,
            "topic": topic,
            "score_percentage": topic_percentage,
            "level": level,
            "estimated_time": estimated_time,
            "study_topics": study_topics,
            "practice": practice,
            "status": "Start Here"
        })

    # ========================================================
    # ADD STRONG TOPICS
    # ========================================================

    strong_start = len(learning_path) + 1

    for index, topic_data in enumerate(
        strong_topics,
        start=strong_start
    ):

        topic = topic_data["topic"]
        topic_percentage = topic_data["percentage"]

        learning_path.append({
            "priority": index,
            "topic": topic,
            "score_percentage": topic_percentage,
            "level": "Strong",
            "estimated_time": "30-45 minutes",
            "study_topics": [
                f"Review {topic}",
                f"Explore advanced concepts in {topic}",
                f"Try challenging problems"
            ],
            "practice": [
                "5 advanced questions",
                "2 application-based problems"
            ],
            "status": "Maintain"
        })

    # ========================================================
    # IF NO TOPIC DATA EXISTS
    # ========================================================

    if not learning_path:

        learning_path.append({
            "priority": 1,
            "topic": "General Review",
            "score_percentage": percentage,
            "level": performance,
            "estimated_time": "1-2 hours",
            "study_topics": [
                "Review the uploaded learning material",
                "Revise important concepts",
                "Practice questions from the material"
            ],
            "practice": [
                "10 practice questions",
                "Review incorrect answers"
            ],
            "status": "Start Here"
        })

    # ========================================================
    # LEARNING ORDER
    # ========================================================

    learning_order = [
        item["topic"]
        for item in learning_path
    ]

    # ========================================================
    # FINAL RECOMMENDATION
    # ========================================================

    if weak_topics:

        first_topic = weak_topics[0]["topic"]

        recommendation = (
            f"Start with {first_topic}. "
            f"Your current overall score is "
            f"{percentage}%. "
            "Focus on your weakest topics first, "
            "then move to stronger topics."
        )

    else:

        recommendation = (
            f"Excellent! Your overall score is "
            f"{percentage}%. "
            "You do not have any major weak topics. "
            "Continue with advanced practice."
        )

    # ========================================================
    # RETURN COMPLETE ANALYSIS
    # ========================================================

    return {
        "score": score,
        "total_questions": total_questions,
        "percentage": percentage,
        "performance": performance,
        "recommendation": recommendation,
        "overall_recommendation": overall_recommendation,
        "weak_topics": [
            item["topic"]
            for item in weak_topics
        ],
        "strong_topics": [
            item["topic"]
            for item in strong_topics
        ],
        "learning_order": learning_order,
        "learning_path": learning_path
    }


# ============================================================
# ADAPTIVE LEARNING PATH ADJUSTMENT
# ============================================================

def create_adaptive_learning_path(
    adaptive_analysis
):
    """
    Create an adaptive learning path from the
    adaptive-learning analysis.

    The path prioritizes weaker topics and adjusts
    difficulty and practice mode according to performance.
    """

    # ========================================================
    # SAFETY CHECK
    # ========================================================

    if not adaptive_analysis:

        return {
            "success": False,
            "learning_path": [],
            "learning_order": [],
            "recommendation": (
                "Complete a quiz to generate an adaptive "
                "learning path."
            )
        }

    topic_adaptations = adaptive_analysis.get(
        "topic_adaptations",
        []
    )

    # ========================================================
    # NO TOPIC DATA
    # ========================================================

    if not topic_adaptations:

        difficulty = adaptive_analysis.get(
            "next_difficulty",
            "Beginner"
        )

        practice_mode = adaptive_analysis.get(
            "practice_mode",
            "Fundamental Practice"
        )

        percentage = adaptive_analysis.get(
            "percentage",
            0
        )

        return {
            "success": True,

            "learning_path": [
                {
                    "priority": 1,
                    "topic": "General Review",
                    "score_percentage": percentage,
                    "level": adaptive_analysis.get(
                        "performance",
                        "No Data"
                    ),
                    "next_difficulty": difficulty,
                    "practice_mode": practice_mode,
                    "estimated_time": "1-2 hours",
                    "study_topics": [
                        "Review the learning material",
                        "Revise important concepts",
                        "Practice questions",
                        "Review incorrect answers"
                    ],
                    "practice": [
                        "10 adaptive questions",
                        "Review incorrect answers"
                    ],
                    "status": "Start Here"
                }
            ],

            "learning_order": [
                "General Review"
            ],

            "recommendation": (
                "Complete topic-based assessments to "
                "activate more personalized adaptive learning."
            )
        }

    # ========================================================
    # CREATE ADAPTIVE PATH
    # ========================================================

    learning_path = []

    for priority, topic_data in enumerate(
        topic_adaptations,
        start=1
    ):

        topic = str(
            topic_data.get(
                "topic",
                "General"
            )
        ).strip()

        if not topic:
            topic = "General"

        percentage = float(
            topic_data.get(
                "percentage",
                0
            )
        )

        performance = topic_data.get(
            "performance",
            "Needs Practice"
        )

        next_difficulty = topic_data.get(
            "next_difficulty",
            "Beginner"
        )

        practice_mode = topic_data.get(
            "practice_mode",
            "Fundamental Practice"
        )

        action = topic_data.get(
            "action",
            "Continue practice"
        )

        # ====================================================
        # WEAK TOPIC
        # ====================================================

        if percentage < 40:

            estimated_time = "2-3 hours"
            status = "Start Here"

            study_topics = [
                f"Understand the fundamentals of {topic}",
                f"Learn the important concepts of {topic}",
                f"Study basic examples of {topic}",
                f"Practice simple problems related to {topic}"
            ]

            practice = [
                "10 beginner questions",
                "5 concept-based questions",
                "Review incorrect answers"
            ]

        # ====================================================
        # NEEDS PRACTICE
        # ====================================================

        elif percentage < 60:

            estimated_time = "1-2 hours"
            status = "Priority Practice"

            study_topics = [
                f"Review important concepts of {topic}",
                f"Study examples related to {topic}",
                f"Identify common mistakes in {topic}",
                "Practice application-based questions"
            ]

            practice = [
                "10 easy questions",
                "5 application-based questions",
                "Review incorrect answers"
            ]

        # ====================================================
        # INTERMEDIATE TOPIC
        # ====================================================

        elif percentage < 80:

            estimated_time = "1 hour"
            status = "Continue"

            study_topics = [
                f"Review intermediate concepts of {topic}",
                f"Study practical examples of {topic}",
                "Solve application-based problems"
            ]

            practice = [
                "5 intermediate questions",
                "5 application-based questions"
            ]

        # ====================================================
        # STRONG TOPIC
        # ====================================================

        else:

            estimated_time = "30-45 minutes"
            status = "Maintain"

            study_topics = [
                f"Review {topic}",
                f"Explore advanced concepts in {topic}",
                "Try challenging problems"
            ]

            practice = [
                "5 advanced questions",
                "2 challenging application problems"
            ]

        # ====================================================
        # ADD ADAPTIVE PATH ITEM
        # ====================================================

        learning_path.append({
            "priority": priority,
            "topic": topic,
            "score_percentage": percentage,
            "performance": performance,
            "level": performance,
            "next_difficulty": next_difficulty,
            "practice_mode": practice_mode,
            "action": action,
            "estimated_time": estimated_time,
            "study_topics": study_topics,
            "practice": practice,
            "status": status
        })

    # ========================================================
    # LEARNING ORDER
    # ========================================================

    learning_order = [
        item["topic"]
        for item in learning_path
    ]

    # ========================================================
    # RECOMMENDATION
    # ========================================================

    first_topic = learning_path[0]

    recommendation = (
        f"Start with {first_topic['topic']}. "
        f"Your topic score is "
        f"{first_topic['score_percentage']}%. "
        f"Next practice should use "
        f"{first_topic['next_difficulty']} difficulty "
        f"through {first_topic['practice_mode']}."
    )

    # ========================================================
    # RETURN ADAPTIVE LEARNING PATH
    # ========================================================

    return {
        "success": True,
        "learning_path": learning_path,
        "learning_order": learning_order,
        "recommendation": recommendation
    }
    
    # ============================================================
# COMPETENCY-BASED PERSONALIZED LEARNING PATH
# ============================================================

def create_competency_learning_path(gap_analysis):
    """
    Create a personalized learning path from the
    competency gap analysis.

    This path is based on:
    - Current competency level
    - Target competency level
    - Skill gap
    - Priority
    """

    # ========================================================
    # SAFETY CHECK
    # ========================================================

    if not gap_analysis:
        return {
            "success": False,
            "learning_path": [],
            "learning_order": [],
            "recommendation": (
                "Complete competency assessment "
                "to generate a personalized learning path."
            )
        }

    if not gap_analysis.get("success"):
        return {
            "success": False,
            "learning_path": [],
            "learning_order": [],
            "recommendation": gap_analysis.get(
                "message",
                "Competency gap analysis is not available."
            )
        }

    skill_gaps = gap_analysis.get(
        "skill_gaps",
        []
    )

    # ========================================================
    # NO SKILL GAPS
    # ========================================================

    if not skill_gaps:

        return {
            "success": True,
            "learning_path": [],
            "learning_order": [],
            "recommendation": (
                "Your competency levels meet the "
                "current framework targets. "
                "Continue with advanced learning "
                "and skill maintenance."
            )
        }

    # ========================================================
    # PRIORITY ORDER
    # ========================================================

    priority_order = {
        "Critical": 1,
        "High": 2,
        "Medium": 3,
        "Low": 4
    }

    skill_gaps = sorted(
        skill_gaps,
        key=lambda item: (
            priority_order.get(
                item.get("priority"),
                99
            ),
            -item.get("gap", 0)
        )
    )

    # ========================================================
    # CREATE LEARNING PATH
    # ========================================================

    learning_path = []

    for index, gap in enumerate(
        skill_gaps,
        start=1
    ):

        skill = gap.get(
            "skill",
            "Unknown Skill"
        )

        category = gap.get(
            "category",
            "General"
        )

        current_level = gap.get(
            "current_level",
            "Beginner"
        )

        target_level = gap.get(
            "target_level",
            "Intermediate"
        )

        priority = gap.get(
            "priority",
            "Medium"
        )

        gap_value = gap.get(
            "gap",
            0
        )

        # ====================================================
        # LEARNING STRATEGY
        # ====================================================

        if current_level == "Beginner":

            estimated_time = "2-3 hours"

            study_topics = [
                f"Learn the fundamentals of {skill}",
                f"Understand the core concepts of {skill}",
                f"Study practical examples of {skill}",
                f"Practice basic problems related to {skill}"
            ]

            practice = [
                "10 beginner questions",
                "5 concept-based questions",
                "Review incorrect answers"
            ]

            level = "Foundation"

        elif current_level == "Intermediate":

            estimated_time = "1-2 hours"

            study_topics = [
                f"Review important concepts of {skill}",
                f"Study intermediate concepts of {skill}",
                f"Work through practical examples of {skill}",
                f"Practice application-based problems"
            ]

            practice = [
                "10 intermediate questions",
                "5 application-based questions",
                "Review incorrect answers"
            ]

            level = "Development"

        elif current_level == "Advanced":

            estimated_time = "1 hour"

            study_topics = [
                f"Review advanced concepts of {skill}",
                f"Study real-world applications of {skill}",
                f"Practice advanced problems related to {skill}"
            ]

            practice = [
                "5 advanced questions",
                "3 application-based problems",
                "Review mistakes"
            ]

            level = "Advanced Development"

        else:

            estimated_time = "30-60 minutes"

            study_topics = [
                f"Review expert-level concepts of {skill}",
                f"Explore advanced applications of {skill}",
                f"Practice challenging problems"
            ]

            practice = [
                "5 expert-level questions",
                "2 challenging application problems"
            ]

            level = "Expert Development"

        # ====================================================
        # STATUS
        # ====================================================

        if priority == "Critical":
            status = "Start Immediately"

        elif priority == "High":
            status = "Start Next"

        elif priority == "Medium":
            status = "Planned"

        else:
            status = "Later"

        # ====================================================
        # ADD PATH ITEM
        # ====================================================

        learning_path.append({
            "priority": index,
            "skill": skill,
            "category": category,
            "current_level": current_level,
            "target_level": target_level,
            "gap": gap_value,
            "priority_level": priority,
            "learning_level": level,
            "estimated_time": estimated_time,
            "study_topics": study_topics,
            "practice": practice,
            "status": status
        })

    # ========================================================
    # LEARNING ORDER
    # ========================================================

    learning_order = [
        item["skill"]
        for item in learning_path
    ]

    # ========================================================
    # FIRST RECOMMENDATION
    # ========================================================

    first = learning_path[0]

    recommendation = (
        f"Start with {first['skill']}. "
        f"Your current level is "
        f"{first['current_level']} and the required "
        f"level is {first['target_level']}. "
        f"This is a {first['priority_level'].lower()} "
        f"priority competency gap."
    )

    # ========================================================
    # RETURN RESULT
    # ========================================================

    return {
        "success": True,
        "learning_path": learning_path,
        "learning_order": learning_order,
        "recommendation": recommendation,
        "job_role": gap_analysis.get(
            "summary",
            {}
        ).get(
            "job_role"
        ),
        "summary": gap_analysis.get(
            "summary",
            {}
        )
    }