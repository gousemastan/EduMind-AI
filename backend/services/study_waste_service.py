from typing import List, Dict, Any


def analyze_study_waste(
    question_times: List[Dict[str, Any]],
    total_session_time: float = 0
) -> Dict[str, Any]:
    """
    Analyze how efficiently a student is spending time on quiz questions.

    Each question should contain:
    {
        "question": "...",
        "topic": "...",
        "time_spent": 45,
        "is_correct": True
    }
    """

    if not question_times:
        return {
            "success": False,
            "message": "No study-time data available."
        }

    total_questions = len(question_times)

    total_question_time = sum(
        float(item.get("time_spent", 0))
        for item in question_times
    )

    average_time = (
        total_question_time / total_questions
        if total_questions > 0
        else 0
    )

    # Questions taking more than 2× the average are considered
    # potential time-waste questions.
    waste_threshold = max(120, average_time * 2)

    waste_questions = []
    efficient_questions = []

    for index, item in enumerate(question_times):
        time_spent = float(item.get("time_spent", 0))

        question_data = {
            "question_number": index + 1,
            "question": item.get("question", ""),
            "topic": item.get("topic", "General"),
            "time_spent": round(time_spent, 2),
            "is_correct": bool(item.get("is_correct", False))
        }

        if time_spent > waste_threshold:
            waste_questions.append(question_data)
        else:
            efficient_questions.append(question_data)

    wasted_time = sum(
        max(0, item["time_spent"] - average_time)
        for item in waste_questions
    )

    efficiency_percentage = (
        (len(efficient_questions) / total_questions) * 100
        if total_questions > 0
        else 0
    )

    # Determine overall status
    waste_ratio = len(waste_questions) / total_questions

    if waste_ratio >= 0.5:
        waste_level = "High"
        recommendation = (
            "You are spending too much time on several questions. "
            "Use targeted explanations and move to focused practice."
        )
    elif waste_ratio >= 0.25:
        waste_level = "Medium"
        recommendation = (
            "Some questions are taking longer than necessary. "
            "Review difficult concepts briefly before trying again."
        )
    else:
        waste_level = "Low"
        recommendation = (
            "Your study time is being used efficiently. "
            "Continue with your current learning strategy."
        )

    # Find topics where the student is spending the most time
    topic_times = {}

    for item in question_times:
        topic = item.get("topic", "General")
        time_spent = float(item.get("time_spent", 0))

        topic_times[topic] = topic_times.get(topic, 0) + time_spent

    top_time_topic = None

    if topic_times:
        top_time_topic = max(
            topic_times,
            key=topic_times.get
        )

    return {
        "success": True,
        "total_questions": total_questions,
        "total_question_time": round(total_question_time, 2),
        "average_time_per_question": round(average_time, 2),
        "waste_threshold": round(waste_threshold, 2),
        "wasted_time": round(wasted_time, 2),
        "efficiency_percentage": round(efficiency_percentage, 2),
        "waste_level": waste_level,
        "waste_questions": waste_questions,
        "efficient_questions": efficient_questions,
        "topic_times": {
            topic: round(time, 2)
            for topic, time in topic_times.items()
        },
        "most_time_consuming_topic": top_time_topic,
        "recommendation": recommendation
    }