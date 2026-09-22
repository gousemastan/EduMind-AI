# ============================================================
# EDUMIND AI
# QUIZ SERVICE
# GEMINI VERSION + LOCAL FALLBACK
# ============================================================

import os
import json
import re
import time
from typing import Any

from dotenv import load_dotenv
from google import genai


# ============================================================
# ENVIRONMENT
# ============================================================

load_dotenv()


# ============================================================
# GEMINI CONFIGURATION
# ============================================================

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

GEMINI_MODEL = os.getenv(
    "GEMINI_MODEL",
    "gemini-3.6-flash"
)

GEMINI_FALLBACK_MODEL = os.getenv(
    "GEMINI_FALLBACK_MODEL",
    "gemini-3.5-flash"
)


# ============================================================
# RETRY CONFIGURATION
# ============================================================

# Maximum Gemini attempts.
#
# Attempt 1
# Wait
# Attempt 2
#
MAX_RETRIES = 2

# Delay for temporary errors such as 503.
RETRY_DELAY_SECONDS = 8


# ============================================================
# GEMINI CLIENT
# ============================================================

_gemini_client = None


def get_gemini_client():
    """
    Create Gemini client only when needed.
    """

    global _gemini_client

    if _gemini_client is not None:
        return _gemini_client

    if not GEMINI_API_KEY:

        raise RuntimeError(
            "GEMINI_API_KEY is missing. "
            "Please add GEMINI_API_KEY to backend/.env"
        )

    try:

        _gemini_client = genai.Client(
            api_key=GEMINI_API_KEY
        )

        return _gemini_client

    except Exception as error:

        raise RuntimeError(
            f"Failed to initialize Gemini client: {error}"
        ) from error


# ============================================================
# HELPER - DETECT TEMPORARY GEMINI ERRORS
# ============================================================

def is_temporary_gemini_error(
    error: Exception
) -> bool:
    """
    Check whether Gemini returned a temporary error
    such as HTTP 503.
    """

    message = str(error).lower()

    temporary_keywords = [

        "503",

        "unavailable",

        "high demand",

        "temporarily unavailable",

        "service unavailable",

        "overloaded",

        "deadline exceeded",

        "timeout",

    ]

    return any(
        keyword in message
        for keyword in temporary_keywords
    )


# ============================================================
# HELPER - DETECT GEMINI QUOTA ERRORS
# ============================================================

def is_quota_error(
    error: Exception
) -> bool:
    """
    Check whether Gemini quota has been exhausted.
    """

    message = str(error).lower()

    return (
        "429" in message
        or "resource_exhausted" in message
        or "quota exceeded" in message
        or "generaterequestsperdayperproject-freetier" in message
    )


# ============================================================
# HELPER - EXTRACT JSON
# ============================================================

def extract_json_from_response(
    response_text: str
) -> Any:
    """
    Extract JSON from Gemini response.

    Supports:

    1. Pure JSON
    2. ```json ... ```
    3. JSON embedded inside normal text
    """

    if not response_text:

        raise ValueError(
            "Gemini returned an empty response."
        )

    text = response_text.strip()

    # --------------------------------------------------------
    # Remove Markdown code fences
    # --------------------------------------------------------

    text = re.sub(
        r"^```json\s*",
        "",
        text,
        flags=re.IGNORECASE
    )

    text = re.sub(
        r"^```\s*",
        "",
        text
    )

    text = re.sub(
        r"\s*```$",
        "",
        text
    )

    text = text.strip()

    # --------------------------------------------------------
    # Try direct JSON
    # --------------------------------------------------------

    try:

        return json.loads(text)

    except json.JSONDecodeError:

        pass

    # --------------------------------------------------------
    # Try JSON array
    # --------------------------------------------------------

    first_array = text.find("[")

    last_array = text.rfind("]")

    if (
        first_array != -1
        and
        last_array != -1
        and
        last_array > first_array
    ):

        candidate = text[
            first_array:last_array + 1
        ]

        try:

            return json.loads(candidate)

        except json.JSONDecodeError:

            pass

    # --------------------------------------------------------
    # Try JSON object
    # --------------------------------------------------------

    first_object = text.find("{")

    last_object = text.rfind("}")

    if (
        first_object != -1
        and
        last_object != -1
        and
        last_object > first_object
    ):

        candidate = text[
            first_object:last_object + 1
        ]

        try:

            return json.loads(candidate)

        except json.JSONDecodeError:

            pass

    # --------------------------------------------------------
    # Failed
    # --------------------------------------------------------

    raise ValueError(
        "Gemini returned a response, "
        "but valid JSON could not be extracted."
    )


# ============================================================
# HELPER - VALIDATE QUIZ
# ============================================================

def validate_quiz(
    quiz: Any,
    expected_questions: int
) -> list:
    """
    Validate Gemini generated quiz structure.
    """

    if not isinstance(
        quiz,
        list
    ):

        raise ValueError(
            "Gemini quiz response must be a JSON array."
        )

    if not quiz:

        raise ValueError(
            "Gemini returned an empty quiz."
        )

    valid_questions = []

    for index, question in enumerate(
        quiz
    ):

        # ----------------------------------------------------
        # Question must be object
        # ----------------------------------------------------

        if not isinstance(
            question,
            dict
        ):

            raise ValueError(
                f"Question {index + 1} "
                f"is not a valid object."
            )

        # ----------------------------------------------------
        # Required fields
        # ----------------------------------------------------

        required_fields = [

            "question",

            "options",

            "correct_answer",

            "explanation",

            "topic",

        ]

        for field in required_fields:

            if field not in question:

                raise ValueError(
                    f"Question {index + 1} "
                    f"is missing required field: "
                    f"{field}"
                )

        # ----------------------------------------------------
        # Question text
        # ----------------------------------------------------

        if not isinstance(
            question["question"],
            str
        ):

            raise ValueError(
                f"Question {index + 1} "
                f"has invalid question text."
            )

        if not question[
            "question"
        ].strip():

            raise ValueError(
                f"Question {index + 1} "
                f"has empty question text."
            )

        # ----------------------------------------------------
        # Options
        # ----------------------------------------------------

        options = question[
            "options"
        ]

        if not isinstance(
            options,
            list
        ):

            raise ValueError(
                f"Question {index + 1} "
                f"options must be a list."
            )

        if len(options) != 4:

            raise ValueError(
                f"Question {index + 1} "
                f"must contain exactly 4 options."
            )

        cleaned_options = []

        for option in options:

            if not isinstance(
                option,
                str
            ):

                raise ValueError(
                    f"Question {index + 1} "
                    f"contains an invalid option."
                )

            if not option.strip():

                raise ValueError(
                    f"Question {index + 1} "
                    f"contains an empty option."
                )

            cleaned_options.append(
                option.strip()
            )

        # ----------------------------------------------------
        # Correct answer
        # ----------------------------------------------------

        correct_answer = question[
            "correct_answer"
        ]

        if not isinstance(
            correct_answer,
            str
        ):

            raise ValueError(
                f"Question {index + 1} "
                f"has an invalid correct_answer."
            )

        if (
            correct_answer.strip()
            not in cleaned_options
        ):

            raise ValueError(
                f"Question {index + 1} "
                f"correct_answer does not "
                f"match any option."
            )

        # ----------------------------------------------------
        # Explanation
        # ----------------------------------------------------

        explanation = question[
            "explanation"
        ]

        if not isinstance(
            explanation,
            str
        ):

            raise ValueError(
                f"Question {index + 1} "
                f"has invalid explanation."
            )

        # ----------------------------------------------------
        # Topic
        # ----------------------------------------------------

        topic = question[
            "topic"
        ]

        if not isinstance(
            topic,
            str
        ):

            topic = "General"

        if not topic.strip():

            topic = "General"

        # ----------------------------------------------------
        # ID
        # ----------------------------------------------------

        question_id = question.get(
            "id",
            f"q{index + 1}"
        )

        # ----------------------------------------------------
        # Clean question
        # ----------------------------------------------------

        cleaned_question = {

            "id":
                str(question_id),

            "question":
                question[
                    "question"
                ].strip(),

            "options":
                cleaned_options,

            "correct_answer":
                correct_answer.strip(),

            "explanation":
                explanation.strip(),

            "topic":
                topic.strip(),

        }

        valid_questions.append(
            cleaned_question
        )

    # ========================================================
    # QUESTION COUNT
    # ========================================================

    if len(valid_questions) < expected_questions:

        raise ValueError(
            f"Gemini returned only "
            f"{len(valid_questions)} valid questions. "
            f"Expected {expected_questions}."
        )

    # --------------------------------------------------------
    # Remove extra questions
    # --------------------------------------------------------

    if len(valid_questions) > expected_questions:

        valid_questions = valid_questions[
            :expected_questions
        ]

    return valid_questions


# ============================================================
# LOCAL FALLBACK QUIZ
# ============================================================

def generate_local_fallback_quiz(
    text: str,
    num_questions: int,
    language: str = "English"
) -> list:
    """
    Generate a local fallback quiz.

    This is used when Gemini quota is exhausted.

    The fallback prevents the complete demo from failing.
    """

    print()
    print("=" * 60)
    print("🛟 LOCAL FALLBACK QUIZ")
    print("=" * 60)

    # --------------------------------------------------------
    # English fallback
    # --------------------------------------------------------

    fallback_questions = [

        {
            "id": "local_q1",

            "question":
                "What is the main purpose of Artificial Intelligence?",

            "options": [

                "Perform intelligent tasks",

                "Only store files",

                "Only print documents",

                "Only display images"

            ],

            "correct_answer":
                "Perform intelligent tasks",

            "explanation":
                "Artificial Intelligence is used to perform tasks that normally require intelligent decision-making.",

            "topic":
                "Artificial Intelligence"
        },

        {
            "id": "local_q2",

            "question":
                "Which technology allows computers to learn from data?",

            "options": [

                "Machine Learning",

                "Word Processing",

                "File Compression",

                "Screen Recording"

            ],

            "correct_answer":
                "Machine Learning",

            "explanation":
                "Machine Learning allows computer systems to learn patterns from data.",

            "topic":
                "Machine Learning"
        },

        {
            "id": "local_q3",

            "question":
                "Which of the following is related to Artificial Intelligence?",

            "options": [

                "Natural Language Processing",

                "Keyboard Cleaning",

                "Cable Management",

                "Screen Brightness"

            ],

            "correct_answer":
                "Natural Language Processing",

            "explanation":
                "Natural Language Processing is an important area of Artificial Intelligence.",

            "topic":
                "Natural Language Processing"
        },

        {
            "id": "local_q4",

            "question":
                "What does an AI model generally use to learn patterns?",

            "options": [

                "Data",

                "Paper",

                "Keyboard",

                "Printer"

            ],

            "correct_answer":
                "Data",

            "explanation":
                "AI and machine-learning systems commonly learn patterns from data.",

            "topic":
                "Machine Learning"
        },

        {
            "id": "local_q5",

            "question":
                "Which field focuses on enabling computers to understand human language?",

            "options": [

                "Natural Language Processing",

                "Computer Assembly",

                "Network Cabling",

                "Disk Formatting"

            ],

            "correct_answer":
                "Natural Language Processing",

            "explanation":
                "Natural Language Processing deals with processing and understanding human language.",

            "topic":
                "Natural Language Processing"
        }

    ]

    # --------------------------------------------------------
    # Telugu fallback
    # --------------------------------------------------------

    telugu_questions = [

        {
            "id": "local_q1",

            "question":
                "Artificial Intelligence యొక్క ప్రధాన ఉద్దేశ్యం ఏమిటి?",

            "options": [

                "తెలివైన పనులను నిర్వహించడం",

                "ఫైళ్లను మాత్రమే నిల్వ చేయడం",

                "డాక్యుమెంట్లను మాత్రమే ప్రింట్ చేయడం",

                "చిత్రాలను మాత్రమే చూపించడం"

            ],

            "correct_answer":
                "తెలివైన పనులను నిర్వహించడం",

            "explanation":
                "Artificial Intelligence సాధారణంగా మానవ తెలివితేటలు అవసరమయ్యే పనులను నిర్వహించడానికి ఉపయోగించబడుతుంది.",

            "topic":
                "Artificial Intelligence"
        },

        {
            "id": "local_q2",

            "question":
                "కంప్యూటర్లు డేటా నుండి నేర్చుకోవడానికి ఏ సాంకేతికత ఉపయోగపడుతుంది?",

            "options": [

                "Machine Learning",

                "Word Processing",

                "File Compression",

                "Screen Recording"

            ],

            "correct_answer":
                "Machine Learning",

            "explanation":
                "Machine Learning డేటా నుండి నమూనాలను నేర్చుకోవడానికి కంప్యూటర్లకు సహాయపడుతుంది.",

            "topic":
                "Machine Learning"
        },

        {
            "id": "local_q3",

            "question":
                "క్రింది వాటిలో Artificial Intelligence కు సంబంధించినది ఏది?",

            "options": [

                "Natural Language Processing",

                "Keyboard Cleaning",

                "Cable Management",

                "Screen Brightness"

            ],

            "correct_answer":
                "Natural Language Processing",

            "explanation":
                "Natural Language Processing అనేది Artificial Intelligence లోని ముఖ్యమైన విభాగం.",

            "topic":
                "Natural Language Processing"
        },

        {
            "id": "local_q4",

            "question":
                "AI మోడల్ సాధారణంగా నమూనాలను నేర్చుకోవడానికి దేనిని ఉపయోగిస్తుంది?",

            "options": [

                "డేటా",

                "పేపర్",

                "కీబోర్డ్",

                "ప్రింటర్"

            ],

            "correct_answer":
                "డేటా",

            "explanation":
                "AI మరియు Machine Learning వ్యవస్థలు సాధారణంగా డేటా నుండి నమూనాలను నేర్చుకుంటాయి.",

            "topic":
                "Machine Learning"
        },

        {
            "id": "local_q5",

            "question":
                "మానవ భాషను కంప్యూటర్లు అర్థం చేసుకోవడానికి సంబంధించిన విభాగం ఏది?",

            "options": [

                "Natural Language Processing",

                "Computer Assembly",

                "Network Cabling",

                "Disk Formatting"

            ],

            "correct_answer":
                "Natural Language Processing",

            "explanation":
                "Natural Language Processing మానవ భాషను ప్రాసెస్ చేయడం మరియు అర్థం చేసుకోవడం గురించి ఉంటుంది.",

            "topic":
                "Natural Language Processing"
        }

    ]

    # --------------------------------------------------------
    # Hindi fallback
    # --------------------------------------------------------

    hindi_questions = [

        {
            "id": "local_q1",

            "question":
                "Artificial Intelligence का मुख्य उद्देश्य क्या है?",

            "options": [

                "बुद्धिमान कार्य करना",

                "केवल फाइलें संग्रहीत करना",

                "केवल दस्तावेज प्रिंट करना",

                "केवल चित्र दिखाना"

            ],

            "correct_answer":
                "बुद्धिमान कार्य करना",

            "explanation":
                "Artificial Intelligence का उपयोग ऐसे कार्य करने के लिए किया जाता है जिनमें सामान्यतः बुद्धिमान निर्णय की आवश्यकता होती है.",

            "topic":
                "Artificial Intelligence"
        },

        {
            "id": "local_q2",

            "question":
                "कंप्यूटर को डेटा से सीखने में कौन सी तकनीक मदद करती है?",

            "options": [

                "Machine Learning",

                "Word Processing",

                "File Compression",

                "Screen Recording"

            ],

            "correct_answer":
                "Machine Learning",

            "explanation":
                "Machine Learning कंप्यूटर सिस्टम को डेटा से पैटर्न सीखने में मदद करता है.",

            "topic":
                "Machine Learning"
        },

        {
            "id": "local_q3",

            "question":
                "इनमें से कौन Artificial Intelligence से संबंधित है?",

            "options": [

                "Natural Language Processing",

                "Keyboard Cleaning",

                "Cable Management",

                "Screen Brightness"

            ],

            "correct_answer":
                "Natural Language Processing",

            "explanation":
                "Natural Language Processing Artificial Intelligence का एक महत्वपूर्ण क्षेत्र है.",

            "topic":
                "Natural Language Processing"
        },

        {
            "id": "local_q4",

            "question":
                "AI मॉडल पैटर्न सीखने के लिए सामान्यतः किसका उपयोग करता है?",

            "options": [

                "डेटा",

                "कागज",

                "कीबोर्ड",

                "प्रिंटर"

            ],

            "correct_answer":
                "डेटा",

            "explanation":
                "AI और Machine Learning सिस्टम सामान्यतः डेटा से पैटर्न सीखते हैं.",

            "topic":
                "Machine Learning"
        },

        {
            "id": "local_q5",

            "question":
                "कंप्यूटर को मानव भाषा समझने से संबंधित क्षेत्र कौन सा है?",

            "options": [

                "Natural Language Processing",

                "Computer Assembly",

                "Network Cabling",

                "Disk Formatting"

            ],

            "correct_answer":
                "Natural Language Processing",

            "explanation":
                "Natural Language Processing मानव भाषा को संसाधित और समझने से संबंधित है.",

            "topic":
                "Natural Language Processing"
        }

    ]

    # --------------------------------------------------------
    # Select language
    # --------------------------------------------------------

    if language.lower() == "telugu":

        selected_questions = telugu_questions

    elif language.lower() == "hindi":

        selected_questions = hindi_questions

    else:

        selected_questions = fallback_questions

    # --------------------------------------------------------
    # Requested number
    # --------------------------------------------------------

    quiz = selected_questions[
        :num_questions
    ]

    print(
        "🌐 Fallback language:",
        language
    )

    print(
        "📊 Fallback questions:",
        len(quiz)
    )

    print("=" * 60)

    return quiz


# ============================================================
# GEMINI QUIZ REQUEST
# ============================================================

def generate_quiz_with_gemini(
    text: str,
    num_questions: int,
    language: str = "English",
    difficulty: str = "Intermediate"
) -> list:
    """
    Send one quiz-generation request to Gemini.

    This function itself performs NO retry.
    Retry is handled by create_quiz().
    """

    client = get_gemini_client()

    print()
    print("=" * 60)
    print("🤖 GEMINI QUIZ REQUEST")
    print("=" * 60)

    print(
        "🧠 Model:",
        GEMINI_MODEL
    )

    print(
        "🌐 Language:",
        language
    )
    
    print(
    "🎯 Difficulty:",
    difficulty
)

    print(
        "📡 Sending request to Gemini..."
    )

    # ========================================================
    # PROMPT
    # ========================================================

    prompt = f"""
You are EduMind AI, an expert educational quiz generator.

Create exactly {num_questions} multiple-choice questions
from the supplied learning material.

LANGUAGE REQUIREMENT:

Generate the entire quiz in {language}.

DIFFICULTY REQUIREMENT:

Generate questions at the {difficulty} difficulty level.

Difficulty guidelines:

- Beginner: test basic definitions, simple concepts, and fundamental understanding.
- Easy: test basic application with limited reasoning.
- Intermediate: require moderate application and understanding.
- Advanced: require deeper reasoning, analysis, application, and challenging concepts.

Do not make the questions easier or harder than the requested difficulty level.

The question, all 4 options, correct_answer,
explanation, and topic must be written in {language}.

Use the selected language consistently.

IMPORTANT RULES:

1. Use ONLY information from the supplied learning material.
2. Do not invent facts.
3. Create exactly {num_questions} questions.
4. Each question must have exactly 4 options.
5. There must be exactly one correct answer.
6. The correct_answer must exactly match one option.
7. Provide a short explanation.
8. Provide a topic for every question.
9. Return ONLY valid JSON.
10. Do NOT use Markdown.
11. Do NOT add introductory text.
12. Do NOT add ```json code fences.

Required JSON structure:

[
  {{
    "id": "q1",
    "question": "Question text",
    "options": [
      "Option 1",
      "Option 2",
      "Option 3",
      "Option 4"
    ],
    "correct_answer": "Option 1",
    "explanation": "Short explanation",
    "topic": "Topic name"
  }}
]

LEARNING MATERIAL:

{text}
"""

    try:

            # ====================================================
            # PRIMARY GEMINI REQUEST
            # ====================================================

            response = client.models.generate_content(
                model=GEMINI_MODEL,
                contents=prompt,
            )

    except Exception as primary_error:

            print()
            print("⚠️ Primary Gemini model failed.")
            print(f"❌ Primary model: {GEMINI_MODEL}")
            print(f"❌ Error: {primary_error}")

            print()
            print("🔄 Trying Gemini fallback model...")
            print(f"🤖 Fallback model: {GEMINI_FALLBACK_MODEL}")

            try:

                # ====================================================
                # FALLBACK GEMINI REQUEST
                # ====================================================

                response = client.models.generate_content(
                    model=GEMINI_FALLBACK_MODEL,
                    contents=prompt,
                )

                print("✅ Fallback Gemini model succeeded.")

            except Exception as fallback_error:

                print()
                print("❌ Fallback Gemini model also failed.")
                print(f"❌ Error: {fallback_error}")

                raise RuntimeError(
                    f"Primary Gemini model failed: {primary_error}. "
                    f"Fallback Gemini model also failed: {fallback_error}"
                ) from fallback_error    
    # ========================================================
    # RESPONSE TEXT
    # ========================================================

    response_text = getattr(
        response,
        "text",
        None
    )

    if not response_text:

        raise RuntimeError(
            "Gemini returned an empty response."
        )

    print(
        "✅ Gemini response received."
    )

    print(
        "📦 Response characters:",
        len(response_text)
    )

    # ========================================================
    # JSON
    # ========================================================

    try:

        quiz_data = extract_json_from_response(
            response_text
        )

    except Exception as error:

        raise ValueError(
            f"Gemini JSON validation failed: {error}"
        ) from error

    print(
        "✅ JSON detected."
    )

    # ========================================================
    # VALIDATE
    # ========================================================

    quiz = validate_quiz(
        quiz_data,
        num_questions
    )

    print()
    print(
        "✅ Quiz validation successful."
    )

    print(
        "📊 Valid questions:",
        len(quiz)
    )

    return quiz


# ============================================================
# MAIN QUIZ FUNCTION
# ============================================================

def create_quiz(
    text: str,
    num_questions: int = 5,
    language: str = "English",
    difficulty: str = "Intermediate"
) -> list:
    """
    Main quiz-generation function.

    Features:

    - Input validation
    - Gemini generation
    - Automatic retry
    - 503 handling
    - 429 quota detection
    - Local fallback
    - JSON validation
    - Quiz validation
    - Multilingual support
    """
    
    
    
        # ========================================================
    # DIFFICULTY VALIDATION
    # ========================================================

    allowed_difficulties = [
        "Beginner",
        "Easy",
        "Intermediate",
        "Advanced"
    ]

    difficulty = str(
        difficulty
    ).strip().title()

    if difficulty not in allowed_difficulties:

        raise ValueError(
            "Difficulty must be "
            "Beginner, Easy, Intermediate, "
            "or Advanced."
        )

    # ========================================================
    # INPUT VALIDATION
    # ========================================================

    if not text or not text.strip():

        raise ValueError(
            "Quiz source text cannot be empty."
        )

    if num_questions < 1:

        raise ValueError(
            "Number of questions must be at least 1."
        )

    if num_questions > 20:

        raise ValueError(
            "Maximum 20 questions are allowed."
        )

    # ========================================================
    # CLEAN TEXT
    # ========================================================

    source_text = text.strip()

    print()
    print("=" * 60)
    print("📝 EDUMIND AI QUIZ SERVICE")
    print("=" * 60)

    print(
        "📄 Source characters:",
        len(source_text)
    )

    print(
        "❓ Requested questions:",
        num_questions
    )

    print(
        "🌐 Language:",
        language
    )
    print(
    "🎯 Difficulty:",
    difficulty
)

    # ========================================================
    # RETRY LOOP
    # ========================================================

    last_error = None

    for attempt in range(
        1,
        MAX_RETRIES + 1
    ):

        print()

        print(
            f"🔄 Gemini attempt "
            f"{attempt}/{MAX_RETRIES}"
        )

        try:

            # ------------------------------------------------
            # ONE GEMINI REQUEST
            # ------------------------------------------------

            quiz = generate_quiz_with_gemini(

                source_text,

                num_questions,

                language,
                
                difficulty

            )

            # ------------------------------------------------
            # SUCCESS
            # ------------------------------------------------

            print()
            print(
                "🎯 Quiz generation completed."
            )

            print("=" * 60)

            return quiz

        except Exception as error:

            last_error = error

            print()
            print(
                f"❌ Quiz attempt {attempt} failed:"
            )

            print(error)

            # =================================================
            # QUOTA ERROR
            # =================================================

            if is_quota_error(error):

                print()
                print(
                    "⚠️ Gemini quota exhausted."
                )

                print(
                    "🔄 Switching to local fallback quiz..."
                )

                fallback_quiz = (
                    generate_local_fallback_quiz(
                        source_text,
                        num_questions,
                        language
                    )
                )

                print()
                print(
                    "✅ Local fallback quiz generated."
                )

                print("=" * 60)

                return fallback_quiz

            # =================================================
            # FINAL ATTEMPT
            # =================================================

            if attempt >= MAX_RETRIES:

                break

            # =================================================
            # TEMPORARY ERROR
            # =================================================

            if is_temporary_gemini_error(error):

                print()
                print(
                    "⚠️ Gemini is temporarily unavailable."
                )

                print(
                    "⏳ Waiting "
                    f"{RETRY_DELAY_SECONDS} seconds "
                    "before retry..."
                )

                time.sleep(
                    RETRY_DELAY_SECONDS
                )

                continue

            # =================================================
            # JSON / VALIDATION ERROR
            # =================================================

            if isinstance(
                error,
                ValueError
            ):

                print()
                print(
                    "⚠️ Quiz response validation failed."
                )

                print(
                    "⏳ Retrying once with Gemini..."
                )

                time.sleep(
                    3
                )

                continue

            # =================================================
            # OTHER ERROR
            # =================================================

            print()
            print(
                "⚠️ Unexpected Gemini error."
            )

            print(
                "⏳ Retrying once..."
            )

            time.sleep(
                3
            )

    # ========================================================
    # FINAL FAILURE
    # ========================================================

    error_message = (
        str(last_error)
        if last_error
        else
        "Unknown Gemini error"
    )

        # ========================================================
    # TEMPORARY 503 FAILURE → LOCAL FALLBACK
    # ========================================================

    if (
        last_error
        and
        is_temporary_gemini_error(
            last_error
        )
    ):

        print()
        print(
            "⚠️ Gemini is still unavailable "
            "after all retry attempts."
        )

        print(
            " Switching to local fallback quiz..."
        )

        try:

            fallback_quiz = (
                generate_local_fallback_quiz(
                    source_text,
                    num_questions,
                    language
                )
            )

            print()
            print(
                " Local fallback quiz generated "
                "successfully."
            )

            print("=" * 60)

            return fallback_quiz

        except Exception as fallback_error:

            print()
            print(
                " Local fallback quiz also failed:"
            )

            print(
                fallback_error
            )

            raise RuntimeError(

                "Gemini AI is temporarily unavailable "
                "and local quiz generation also failed."
            ) from fallback_error
    # ========================================================
    # OTHER FAILURE
    # ========================================================

    raise RuntimeError(

        "Quiz generation failed after "
        f"{MAX_RETRIES} attempts: "
        f"{error_message}"
    )