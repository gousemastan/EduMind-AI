# ============================================================
# EDUMIND AI
# CONFUSION DETECTOR SERVICE
# ============================================================

import os
import json
import re

from dotenv import load_dotenv
from google import genai

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

GEMINI_MODEL = os.getenv(
    "GEMINI_MODEL",
    "gemini-3.6-flash"
)

client = None

if GEMINI_API_KEY:
    try:
        client = genai.Client(
            api_key=GEMINI_API_KEY
        )

        print("✅ Confusion Detector Gemini client initialized.")

    except Exception as error:
        print("⚠️ Confusion Detector Gemini initialization failed:")
        print(error)


# ============================================================
# LOCAL FALLBACK
# ============================================================

def generate_local_confusion_analysis(
    question,
    correct_answer,
    student_answer,
    explanation,
    topic
):
    """
    Local fallback used when Gemini is unavailable.
    """

    explanation_text = explanation.strip()

    student_answer_text = student_answer.strip()
    correct_answer_text = correct_answer.strip()

    # --------------------------------------------------------
    # Empty explanation
    # --------------------------------------------------------

    if not explanation_text:

        return {
            "success": True,
            "understanding_score": 20,
            "confusion_level": "High",
            "understood": [
                "You selected an answer."
            ],
            "missing_concepts": [
                f"You did not explain your reasoning about {topic}."
            ],
            "targeted_explanation": (
                f"Try explaining why {student_answer_text} "
                f"is related to the question. Compare it carefully "
                f"with the concept of {topic}."
            ),
            "practice_questions": [
                f"What is the main idea of {topic}?",
                f"Why is {correct_answer_text} related to this question?",
                f"Explain {topic} using a simple example."
            ]
        }

    # --------------------------------------------------------
    # Basic answer comparison
    # --------------------------------------------------------

    student_correct = (
        student_answer_text.lower()
        == correct_answer_text.lower()
    )

    words = explanation_text.split()

    if student_correct:
        score = min(
            95,
            55 + len(words) * 3
        )
    else:
        score = min(
            65,
            25 + len(words) * 2
        )

    if score >= 80:
        confusion = "Low"

    elif score >= 55:
        confusion = "Medium"

    else:
        confusion = "High"

    # --------------------------------------------------------
    # Fallback response
    # --------------------------------------------------------

    return {
        "success": True,

        "understanding_score": score,

        "confusion_level": confusion,

        "understood": [
            (
                "Your explanation contains "
                f"{len(words)} words and shows an attempt "
                "to reason about the concept."
            )
        ],

        "missing_concepts": [
            (
                f"Review the connection between "
                f"{topic} and the correct answer."
            )
        ],

        "targeted_explanation": (
            f"Focus on the concept of {topic}. "
            f"The expected answer is {correct_answer_text}. "
            "Try to explain the reason, not only the answer."
        ),

        "practice_questions": [
            f"What is {topic}?",
            f"Why is {correct_answer_text} the best answer?",
            f"Give one real-world example of {topic}."
        ]
    }


# ============================================================
# GEMINI ANALYSIS
# ============================================================

def analyze_confusion_with_gemini(
    question,
    correct_answer,
    student_answer,
    explanation,
    topic
):

    if client is None:
        raise RuntimeError(
            "Gemini client is not configured."
        )

    prompt = f"""
You are EduMind AI's Confusion Detection Engine.

Analyze a student's explanation after answering a multiple-choice
question.

Your goal is NOT to judge the student personally.

Your goal is to identify the student's conceptual understanding.

QUESTION:
{question}

TOPIC:
{topic}

CORRECT ANSWER:
{correct_answer}

STUDENT ANSWER:
{student_answer}

STUDENT EXPLANATION:
{explanation}

Analyze:

1. How well does the student understand the concept?
2. What part of the concept does the student understand?
3. What concept is missing or confused?
4. Give a short targeted explanation.
5. Give exactly 3 follow-up practice questions.

Return ONLY valid JSON.

Required structure:

{{
    "understanding_score": 0,
    "confusion_level": "Low",
    "understood": [
        "..."
    ],
    "missing_concepts": [
        "..."
    ],
    "targeted_explanation": "...",
    "practice_questions": [
        "...",
        "...",
        "..."
    ]
}}

Rules:

- understanding_score must be between 0 and 100.
- confusion_level must be Low, Medium, or High.
- Do not invent facts.
- Use simple student-friendly language.
- Focus on the supplied question and topic.
- Do not criticize the student.
- If the student selected the correct answer but gave incorrect
  reasoning, detect the conceptual gap.
- If the student selected the wrong answer but explanation shows
  partial understanding, recognize that partial understanding.
"""

    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt
    )

    response_text = getattr(
        response,
        "text",
        None
    )

    if not response_text:
        raise RuntimeError(
            "Gemini returned an empty confusion analysis."
        )

    # --------------------------------------------------------
    # Remove possible markdown fences
    # --------------------------------------------------------

    response_text = response_text.strip()

    response_text = re.sub(
        r"^```json\s*",
        "",
        response_text,
        flags=re.IGNORECASE
    )

    response_text = re.sub(
        r"\s*```$",
        "",
        response_text
    )

    data = json.loads(
        response_text
    )

    return data


# ============================================================
# MAIN FUNCTION
# ============================================================

def analyze_confusion(
    question,
    correct_answer,
    student_answer,
    explanation,
    topic="General"
):

    question = str(question or "").strip()
    correct_answer = str(correct_answer or "").strip()
    student_answer = str(student_answer or "").strip()
    explanation = str(explanation or "").strip()
    topic = str(topic or "General").strip()

    if not question:
        raise ValueError(
            "Question cannot be empty."
        )

    if not correct_answer:
        raise ValueError(
            "Correct answer cannot be empty."
        )

    if not student_answer:
        raise ValueError(
            "Student answer cannot be empty."
        )

    # --------------------------------------------------------
    # Try Gemini
    # --------------------------------------------------------

    try:

        result = analyze_confusion_with_gemini(
            question,
            correct_answer,
            student_answer,
            explanation,
            topic
        )

        result["success"] = True
        result["provider"] = "Gemini"

        return result

    except Exception as error:

        print()
        print("⚠️ Confusion Detector Gemini failed:")
        print(error)

        print(
            "🔄 Switching to local confusion analysis..."
        )

    # --------------------------------------------------------
    # Local fallback
    # --------------------------------------------------------

    result = generate_local_confusion_analysis(
        question,
        correct_answer,
        student_answer,
        explanation,
        topic
    )

    result["provider"] = "Local Fallback"

    return result