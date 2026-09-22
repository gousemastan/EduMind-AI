import os
import json

from dotenv import load_dotenv
from google import genai

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv(
    "GEMINI_MODEL",
    "gemini-3.6-flash"
)

_client = None


def get_gemini_client():
    global _client

    if _client is not None:
        return _client

    if not GEMINI_API_KEY:
        raise RuntimeError(
            "GEMINI_API_KEY is missing. "
            "Please check backend/.env"
        )

    _client = genai.Client(
        api_key=GEMINI_API_KEY
    )

    return _client


def generate_competency_assessment(
    category: str,
    skill: str,
    current_level: str = "Beginner",
    target_level: str = "Intermediate",
):
    client = get_gemini_client()

    prompt = f"""
You are an AI competency assessment engine for EduMind AI.

Create a competency assessment for a learner.

Category: {category}
Skill: {skill}
Current Level: {current_level}
Target Level: {target_level}

Generate exactly 5 multiple-choice questions.

Requirements:
- Questions must test practical understanding.
- Questions should match the selected skill.
- Difficulty should gradually increase.
- Each question must have exactly 4 options.
- Only one option must be correct.
- Do not reveal the answer in the question.
- Return ONLY valid JSON.

Return this exact JSON structure:

{{
  "category": "{category}",
  "skill": "{skill}",
  "questions": [
    {{
      "question": "Question text",
      "options": [
        "Option 1",
        "Option 2",
        "Option 3",
        "Option 4"
      ],
      "correct_answer": "Option 1"
    }}
  ]
}}
"""

    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt
    )

    if not response or not response.text:
        raise RuntimeError(
            "Gemini returned an empty assessment."
        )

    raw_response = response.text.strip()

    if raw_response.startswith("```"):
        raw_response = raw_response.replace(
            "```json", ""
        ).replace(
            "```", ""
        ).strip()

    try:
        assessment = json.loads(raw_response)
    except json.JSONDecodeError as error:
        print("❌ Gemini assessment JSON error:", error)
        print("📦 Raw response:", raw_response)

        raise RuntimeError(
            "Gemini returned invalid assessment JSON."
        )

    questions = assessment.get("questions", [])

    if len(questions) != 5:
        raise RuntimeError(
            "Gemini did not generate exactly 5 questions."
        )

    return assessment


def evaluate_competency_assessment(
    category: str,
    skill: str,
    questions: list,
    answers: list,
):
    client = get_gemini_client()

    correct_count = 0

    for index, question in enumerate(questions):
        if index >= len(answers):
            continue

        correct_answer = question.get(
            "correct_answer"
        )

        user_answer = answers[index]

        if user_answer == correct_answer:
            correct_count += 1

    total_questions = len(questions)

    percentage = 0

    if total_questions > 0:
        percentage = round(
            (correct_count / total_questions) * 100
        )

    if percentage >= 80:
        assessed_level = "Advanced"
    elif percentage >= 60:
        assessed_level = "Intermediate"
    else:
        assessed_level = "Beginner"

    analysis_prompt = f"""
You are an AI competency analysis engine.

Analyze this learner's competency assessment.

Category: {category}
Skill: {skill}

Total Questions: {total_questions}
Correct Answers: {correct_count}
Percentage: {percentage}%
Assessed Level: {assessed_level}

Provide:
1. A short competency summary.
2. The learner's strengths.
3. The learner's weaknesses.
4. One recommended next learning action.

Return ONLY valid JSON:

{{
  "summary": "Short competency summary",
  "strengths": [
    "Strength 1",
    "Strength 2"
  ],
  "weaknesses": [
    "Weakness 1",
    "Weakness 2"
  ],
  "next_action": "Recommended next learning action"
}}
"""

    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=analysis_prompt
    )

    analysis = {
        "summary": "",
        "strengths": [],
        "weaknesses": [],
        "next_action": ""
    }

    if response and response.text:
        raw_response = response.text.strip()

        if raw_response.startswith("```"):
            raw_response = raw_response.replace(
                "```json", ""
            ).replace(
                "```", ""
            ).strip()

        try:
            analysis = json.loads(raw_response)
        except json.JSONDecodeError:
            print(
                "⚠️ Gemini analysis JSON could not be parsed."
            )

    return {
        "category": category,
        "skill": skill,
        "score": correct_count,
        "total_questions": total_questions,
        "percentage": percentage,
        "assessed_level": assessed_level,
        "analysis": analysis,
    }