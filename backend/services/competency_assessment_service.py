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


# ============================================================
# GEMINI CLIENT
# ============================================================

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


# ============================================================
# LOCAL FALLBACK ASSESSMENT
# ============================================================

def create_local_assessment(
    category: str,
    skill: str,
    current_level: str = "Beginner",
    target_level: str = "Intermediate",
):
    """
    Local competency assessment used when Gemini is unavailable.

    Always returns exactly 5 MCQs with 4 options each.
    """

    skill_lower = skill.lower().strip()

    # --------------------------------------------------------
    # Python
    # --------------------------------------------------------

    if skill_lower == "python":

        questions = [
            {
                "question": "Which keyword is used to define a function in Python?",
                "options": [
                    "function",
                    "def",
                    "func",
                    "define"
                ],
                "correct_answer": "def"
            },
            {
                "question": "Which Python data type stores key-value pairs?",
                "options": [
                    "List",
                    "Tuple",
                    "Dictionary",
                    "Set"
                ],
                "correct_answer": "Dictionary"
            },
            {
                "question": "What is the output of len([10, 20, 30])?",
                "options": [
                    "2",
                    "3",
                    "4",
                    "30"
                ],
                "correct_answer": "3"
            },
            {
                "question": "Which statement is used to handle exceptions in Python?",
                "options": [
                    "try-except",
                    "if-else",
                    "for-while",
                    "switch-case"
                ],
                "correct_answer": "try-except"
            },
            {
                "question": "Which concept allows a class to reuse properties and methods from another class?",
                "options": [
                    "Encapsulation",
                    "Inheritance",
                    "Iteration",
                    "Compilation"
                ],
                "correct_answer": "Inheritance"
            }
        ]

    # --------------------------------------------------------
    # SQL
    # --------------------------------------------------------

    elif skill_lower == "sql":

        questions = [
            {
                "question": "Which SQL statement is used to retrieve data from a table?",
                "options": [
                    "GET",
                    "SELECT",
                    "FETCH",
                    "READ"
                ],
                "correct_answer": "SELECT"
            },
            {
                "question": "Which clause is used to filter rows in SQL?",
                "options": [
                    "ORDER BY",
                    "GROUP BY",
                    "WHERE",
                    "SORT BY"
                ],
                "correct_answer": "WHERE"
            },
            {
                "question": "Which SQL function returns the number of rows?",
                "options": [
                    "SUM()",
                    "COUNT()",
                    "TOTAL()",
                    "NUMBER()"
                ],
                "correct_answer": "COUNT()"
            },
            {
                "question": "Which clause is commonly used to sort SQL query results?",
                "options": [
                    "SORT BY",
                    "ORDER BY",
                    "ARRANGE BY",
                    "GROUP BY"
                ],
                "correct_answer": "ORDER BY"
            },
            {
                "question": "Which SQL operation combines rows from related tables?",
                "options": [
                    "JOIN",
                    "MERGE ROW",
                    "CONNECT",
                    "COMBINE"
                ],
                "correct_answer": "JOIN"
            }
        ]

    # --------------------------------------------------------
    # DATA VISUALIZATION
    # --------------------------------------------------------

    elif "visualization" in skill_lower:

        questions = [
            {
                "question": "What is the main purpose of data visualization?",
                "options": [
                    "Store data",
                    "Communicate patterns and insights",
                    "Delete data",
                    "Encrypt data"
                ],
                "correct_answer": "Communicate patterns and insights"
            },
            {
                "question": "Which chart is commonly used to compare categories?",
                "options": [
                    "Bar chart",
                    "Scatter plot",
                    "Network graph",
                    "Map only"
                ],
                "correct_answer": "Bar chart"
            },
            {
                "question": "Which chart is useful for showing trends over time?",
                "options": [
                    "Line chart",
                    "Pie chart",
                    "Tree diagram",
                    "Histogram only"
                ],
                "correct_answer": "Line chart"
            },
            {
                "question": "Which visualization is commonly used to show the relationship between two numerical variables?",
                "options": [
                    "Scatter plot",
                    "Pie chart",
                    "Bar chart",
                    "Table only"
                ],
                "correct_answer": "Scatter plot"
            },
            {
                "question": "What should a good visualization primarily avoid?",
                "options": [
                    "Clear labels",
                    "Meaningful titles",
                    "Unnecessary visual complexity",
                    "Relevant data"
                ],
                "correct_answer": "Unnecessary visual complexity"
            }
        ]

    # --------------------------------------------------------
    # DATABASE
    # --------------------------------------------------------

    elif "database" in skill_lower:

        questions = [
            {
                "question": "What is a database primarily used for?",
                "options": [
                    "Storing and managing data",
                    "Designing images",
                    "Playing videos",
                    "Writing operating systems"
                ],
                "correct_answer": "Storing and managing data"
            },
            {
                "question": "Which key uniquely identifies a row in a relational table?",
                "options": [
                    "Foreign key",
                    "Primary key",
                    "Duplicate key",
                    "Temporary key"
                ],
                "correct_answer": "Primary key"
            },
            {
                "question": "What is a foreign key used for?",
                "options": [
                    "Encrypting a database",
                    "Connecting related tables",
                    "Deleting all rows",
                    "Sorting columns"
                ],
                "correct_answer": "Connecting related tables"
            },
            {
                "question": "Which operation adds a new row to a table?",
                "options": [
                    "INSERT",
                    "ADDROW",
                    "CREATE ROW",
                    "APPEND TABLE"
                ],
                "correct_answer": "INSERT"
            },
            {
                "question": "Why is database normalization used?",
                "options": [
                    "To reduce unnecessary data duplication",
                    "To increase duplicate records",
                    "To remove all relationships",
                    "To convert tables into images"
                ],
                "correct_answer": "To reduce unnecessary data duplication"
            }
        ]

    # --------------------------------------------------------
    # GENERIC FALLBACK
    # --------------------------------------------------------

    else:

        questions = [
            {
                "question": f"What is the primary purpose of {skill}?",
                "options": [
                    f"Applying {skill} to solve relevant problems",
                    "Deleting all data",
                    "Avoiding practical work",
                    "Replacing every technology"
                ],
                "correct_answer": f"Applying {skill} to solve relevant problems"
            },
            {
                "question": f"Which approach is most useful when learning {skill}?",
                "options": [
                    "Only memorizing definitions",
                    "Practicing concepts with examples",
                    "Avoiding exercises",
                    "Ignoring errors"
                ],
                "correct_answer": "Practicing concepts with examples"
            },
            {
                "question": f"Why is practical knowledge of {skill} important?",
                "options": [
                    "It helps apply concepts to real problems",
                    "It removes the need to learn",
                    "It prevents experimentation",
                    "It eliminates documentation"
                ],
                "correct_answer": "It helps apply concepts to real problems"
            },
            {
                "question": f"What should a learner do after making an error while using {skill}?",
                "options": [
                    "Ignore it",
                    "Delete the project",
                    "Analyze the error and correct it",
                    "Stop learning"
                ],
                "correct_answer": "Analyze the error and correct it"
            },
            {
                "question": f"Which activity best demonstrates competency in {skill}?",
                "options": [
                    "Applying the skill to a practical task",
                    "Memorizing one definition",
                    "Avoiding projects",
                    "Reading without practice"
                ],
                "correct_answer": "Applying the skill to a practical task"
            }
        ]

    return {
        "category": category,
        "skill": skill,
        "current_level": current_level,
        "target_level": target_level,
        "questions": questions,
        "provider": "Local Fallback",
        "model": "Local Competency Assessment"
    }


# ============================================================
# GENERATE COMPETENCY ASSESSMENT
# ============================================================

def generate_competency_assessment(
    category: str,
    skill: str,
    current_level: str = "Beginner",
    target_level: str = "Intermediate",
):

    try:

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
                "```json",
                ""
            ).replace(
                "```",
                ""
            ).strip()

        try:
            assessment = json.loads(raw_response)

        except json.JSONDecodeError as error:

            print(
                "⚠️ Gemini assessment JSON error:",
                error
            )

            raise RuntimeError(
                "Gemini returned invalid assessment JSON."
            )

        questions = assessment.get(
            "questions",
            []
        )

        if len(questions) != 5:
            raise RuntimeError(
                "Gemini did not generate exactly 5 questions."
            )

        print("✅ Gemini competency assessment generated.")

        return assessment

    except Exception as error:

        print(
            "⚠️ Gemini competency assessment unavailable:",
            error
        )

        print(
            "🔄 Using local competency assessment fallback..."
        )

        assessment = create_local_assessment(
            category=category,
            skill=skill,
            current_level=current_level,
            target_level=target_level
        )

        print(
            "✅ Local competency assessment generated."
        )

        return assessment


# ============================================================
# EVALUATE COMPETENCY ASSESSMENT
# ============================================================

def evaluate_competency_assessment(
    category: str,
    skill: str,
    questions: list,
    answers: list,
):

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

    # --------------------------------------------------------
    # LEVEL
    # --------------------------------------------------------

    if percentage >= 80:
        assessed_level = "Advanced"

    elif percentage >= 60:
        assessed_level = "Intermediate"

    else:
        assessed_level = "Beginner"

    # --------------------------------------------------------
    # LOCAL ANALYSIS
    # --------------------------------------------------------

    if percentage >= 80:

        summary = (
            f"You demonstrated strong competency in {skill}."
        )

        strengths = [
            f"Good understanding of {skill}",
            "Strong practical application",
            "Good accuracy in assessment"
        ]

        weaknesses = [
            "Continue practicing advanced concepts"
        ]

        next_action = (
            f"Practice advanced {skill} problems "
            "and real-world projects."
        )

    elif percentage >= 60:

        summary = (
            f"You have a developing understanding of {skill}."
        )

        strengths = [
            f"Basic concepts of {skill} are understood",
            "Some practical understanding is present"
        ]

        weaknesses = [
            f"Some {skill} concepts need more practice",
            "Improve accuracy with practical problems"
        ]

        next_action = (
            f"Review intermediate {skill} concepts "
            "and complete more practical exercises."
        )

    else:

        summary = (
            f"You need more practice with {skill}."
        )

        strengths = [
            "Some foundational understanding is present"
        ]

        weaknesses = [
            f"Core {skill} concepts need reinforcement",
            "More practical practice is required"
        ]

        next_action = (
            f"Review beginner-level {skill} concepts "
            "and practice simple examples."
        )

    analysis = {
        "summary": summary,
        "strengths": strengths,
        "weaknesses": weaknesses,
        "next_action": next_action
    }

    return {
        "category": category,
        "skill": skill,
        "score": correct_count,
        "total_questions": total_questions,
        "percentage": percentage,
        "assessed_level": assessed_level,
        "analysis": analysis,
        "provider": "Local Evaluation",
        "model": "Local Competency Evaluation"
    }