# ============================================================
# EDUMIND AI
# MAIN FASTAPI APPLICATION
# GEMINI VERSION
# ============================================================

from pathlib import Path
import os
import json

from google import genai

from fastapi import (
    FastAPI,
    UploadFile,
    File,
    HTTPException,
    Body,
    Query,
    Depends,
)

from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel, Field

from dotenv import load_dotenv

from auth_utils import get_current_user_id

from services.pdf_service import extract_text_from_pdf
from services.topic_service import detect_topics
from services.quiz_service import create_quiz
from services.tutor_service import ask_ai_tutor
from services.notes_service import generate_ai_notes
from services.flashcard_service import generate_flashcards
from services.confusion_service import analyze_confusion
from services.study_waste_service import analyze_study_waste

from database import init_database
from database import get_connection

from routes.auth_routes import router as auth_router
from routes.history_routes import router as history_router
from routes.competency_routes import router as competency_router
from routes.igot_routes import router as igot_router
from routes.nssta_routes import router as nssta_router
from routes.weak_skill_routes import router as weak_skill_router
from routes.revision_routes import router as revision_router
from routes.adaptive_learning_routes import router as adaptive_learning_router
from routes.admin_routes import router as admin_router

from routes.progress_routes import router as progress_router

from routes.history_routes import router as history_router


# ============================================================
# ENVIRONMENT
# ============================================================

load_dotenv()


# ============================================================
# GEMINI CONFIGURATION
# ============================================================

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

JWT_SECRET_KEY = os.getenv(
    "JWT_SECRET_KEY",
    "edumind-development-secret-change-this"
)

JWT_ALGORITHM = "HS256"

JWT_EXPIRE_MINUTES = 60

GEMINI_MODEL = os.getenv(
    "GEMINI_MODEL",
    "gemini-3.6-flash"
)


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

UPLOAD_DIR = BASE_DIR / "uploads"

UPLOAD_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# ============================================================
# FASTAPI APPLICATION
# ============================================================

app = FastAPI(
    title="EduMind AI",
    description="AI-powered personalized learning platform",
    version="1.0.0"
)


# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,

    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",

        "http://localhost:5174",
        "http://127.0.0.1:5174",
    ],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],
)


# ============================================================
# ROUTERS
# ============================================================

app.include_router(auth_router)
app.include_router(history_router)
app.include_router(competency_router)
app.include_router(igot_router)
app.include_router(nssta_router)
app.include_router(weak_skill_router)
app.include_router(revision_router)
app.include_router(admin_router)

app.include_router(progress_router)


app.include_router(
    adaptive_learning_router
)


# ============================================================
# REQUEST MODELS
# ============================================================

class TutorRequest(BaseModel):

    question: str = Field(
        ...,
        min_length=1
    )

    context: str = ""

    topic: str = "General"


class SkillGapQuestion(BaseModel):

    id: str = ""

    question: str = ""

    answer: str = ""

    topic: str = "General"

    user_answer: str = ""

    is_correct: bool = False


class SkillGapRequest(BaseModel):

    filename: str = ""

    topics: list[str] = Field(
        default_factory=list
    )

    score: int = 0

    total_questions: int = 0

    questions: list[SkillGapQuestion] = Field(
        default_factory=list
    )


class LearningPathRequest(BaseModel):

    score: int = 0

    total_questions: int = 0

    questions: list[SkillGapQuestion] = Field(
        default_factory=list
    )


# ============================================================
# STARTUP
# ============================================================

@app.on_event("startup")
async def startup_event():

    print()

    print("=" * 60)
    print("🚀 EduMind AI Backend")
    print("=" * 60)

    init_database()

    print(
        "🤖 AI Provider :",
        "Gemini"
    )

    print(
        "🧠 AI Model    :",
        GEMINI_MODEL
    )

    print(
        "🔑 API Key     :",
        "Configured"
        if GEMINI_API_KEY
        else "Missing"
    )

    print(
        "📁 Uploads     :",
        UPLOAD_DIR
    )

    print("=" * 60)

    print()


# ============================================================
# HOME
# ============================================================

@app.get("/")
async def home():

    return {
        "success": True,

        "message":
            "Welcome to EduMind AI",

        "version":
            "1.0.0",

        "ai_provider":
            "Gemini",

        "model":
            GEMINI_MODEL,
    }
    
@app.post("/api/generate-flashcards")
async def generate_flashcards_from_uploaded_file(
    filename: str = Query(..., min_length=1),
    number_of_cards: int = Query(10, ge=1, le=20)
):
    try:
        file_path = UPLOAD_DIR / filename

        if not file_path.exists():
            raise HTTPException(
                status_code=404,
                detail="Uploaded PDF not found."
            )

        text = extract_text_from_pdf(str(file_path))

        if not text or not text.strip():
            raise HTTPException(
                status_code=400,
                detail="Could not extract text from PDF."
            )

        flashcards = generate_flashcards(
            text,
            number_of_cards
        )

        return {
            "success": True,
            "message": "AI flashcards generated successfully.",
            "filename": filename,
            "flashcards": flashcards,
            "count": len(flashcards),
            "provider": "Gemini",
            "model": GEMINI_MODEL
        }

    except HTTPException:
        raise

    except Exception as error:
        print("Flashcard Generation Error:", error)

        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate flashcards: {error}"
        )
        
        
@app.post("/api/study-waste-detector")
async def study_waste_detector(data: dict):
    try:
        question_times = data.get("question_times", [])
        total_session_time = data.get("total_session_time", 0)

        result = analyze_study_waste(
            question_times=question_times,
            total_session_time=total_session_time
        )

        return result

    except Exception as e:
        print("❌ Study Waste Detector Error:", e)

        return {
            "success": False,
            "message": str(e)
        }
    
    # ============================================================
# AI NOTES GENERATION
# ============================================================

@app.post("/api/generate-notes")
async def generate_notes_from_uploaded_file(
    filename: str = Query(..., min_length=1),
    language: str = Query("English", min_length=1)

):
    try:
        file_path = UPLOAD_DIR / filename

        if not file_path.exists():
            raise HTTPException(
                status_code=404,
                detail="Uploaded PDF not found."
            )

        text = extract_text_from_pdf(
            str(file_path)
        )

        if not text or not text.strip():
            raise HTTPException(
                status_code=400,
                detail="Could not extract text from PDF."
            )

        notes = generate_ai_notes(
    text,
    language
)
        
        print(
    "🌐 Notes Language:",
    language
)

        return {
            "success": True,
            "message": "AI notes generated successfully.",
            "filename": filename,
            "notes": notes,
            "provider": "Gemini",
            "model": GEMINI_MODEL
        }

    except HTTPException:
        raise

    except Exception as error:
        print("AI Notes Error:", error)

        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate AI notes: {error}"
        )


# ============================================================
# HEALTH
# ============================================================

@app.get("/health")
async def health():

    return {
        "success": True,

        "status":
            "healthy",

        "gemini":
            "configured"
            if GEMINI_API_KEY
            else "missing",

        "model":
            GEMINI_MODEL,
    }





# ============================================================
# API INFORMATION
# ============================================================

@app.get("/api")
async def api_info():

    return {
        "success": True,

        "name":
            "EduMind AI API",

        "version":
            "1.0.0",

        "ai": {
            "provider":
                "Gemini",

            "model":
                GEMINI_MODEL,
        },

        "endpoints": [

            "/",
            "/health",
            "/api",

            "/upload",
            "/api/upload",

            "/quiz",
            "/api/generate-quiz",

            "/quiz/text",

            "/topics",
            "/api/detect-topics",

            "/ai-tutor",

            "/skill-gaps",
            "/api/skill-gaps",

            "/learning-path",
            "/api/learning-path",

            "/api/auth/register",
            "/api/auth/login",
            "/api/auth/me",

            "/api/progress/save",
            "/api/progress/",
        ],
    }


# ============================================================
# COMMON PDF VALIDATION
# ============================================================

def validate_pdf_filename(filename: str):

    if not filename:

        raise HTTPException(
            status_code=400,
            detail="No file selected."
        )

    if not filename.lower().endswith(".pdf"):

        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported."
        )


# ============================================================
# SAFE FILE PATH
# ============================================================

def get_safe_upload_path(filename: str) -> Path:

    # Prevent ../ path traversal
    safe_name = Path(filename).name

    if not safe_name:

        raise HTTPException(
            status_code=400,
            detail="Invalid filename."
        )

    return UPLOAD_DIR / safe_name


# ============================================================
# PDF UPLOAD
#
# POST /upload
# POST /api/upload
# ============================================================

@app.post("/upload")
@app.post("/api/upload")
async def upload_pdf(
    file: UploadFile = File(...)
):

    print()

    print("=" * 60)
    print("📄 EDUMIND AI PDF UPLOAD")
    print("=" * 60)

    # --------------------------------------------------------
    # Validate filename
    # --------------------------------------------------------

    validate_pdf_filename(
        file.filename
    )

    print(
        "📄 Filename:",
        file.filename
    )

    # --------------------------------------------------------
    # Get safe path
    # --------------------------------------------------------

    file_path = get_safe_upload_path(
        file.filename
    )

    # --------------------------------------------------------
    # Read uploaded file
    # --------------------------------------------------------

    try:

        contents = await file.read()

        if not contents:

            raise HTTPException(
                status_code=400,
                detail="Uploaded PDF is empty."
            )

    except HTTPException:

        raise

    except Exception as error:

        print(
            "❌ File read error:",
            error
        )

        raise HTTPException(
            status_code=500,
            detail=f"Failed to read uploaded PDF: {error}"
        )

    # --------------------------------------------------------
    # Save PDF
    # --------------------------------------------------------

    try:

        with open(
            file_path,
            "wb"
        ) as f:

            f.write(contents)

        print(
            "✅ PDF saved:",
            file_path
        )

    except Exception as error:

        print(
            "❌ PDF save error:",
            error
        )

        raise HTTPException(
            status_code=500,
            detail=f"Failed to save PDF: {error}"
        )

    # --------------------------------------------------------
    # Extract text
    # --------------------------------------------------------

    try:

        print(
            "📖 Extracting PDF text..."
        )

        text = extract_text_from_pdf(
            str(file_path)
        )

        if not text or not text.strip():

            raise HTTPException(
                status_code=400,
                detail=(
                    "No readable text found "
                    "in the PDF."
                )
            )

        print(
            "✅ Extracted characters:",
            len(text)
        )

    except HTTPException:

        raise

    except Exception as error:

        print(
            "❌ PDF extraction error:",
            error
        )

        raise HTTPException(
            status_code=500,
            detail=(
                "Failed to extract PDF text: "
                f"{error}"
            )
        )

    # --------------------------------------------------------
    # Detect topics
    # --------------------------------------------------------

    try:

        topics = detect_topics(
            text
        )

        print(
            "🏷️ Topics:",
            topics
        )

    except Exception as error:

        print(
            "⚠️ Topic detection failed:",
            error
        )

        topics = []

    # --------------------------------------------------------
    # Response
    # --------------------------------------------------------

    print(
        "✅ Upload completed successfully."
    )

    print("=" * 60)

    return {

        "success":
            True,

        "message":
            "PDF uploaded successfully.",

        "filename":
            file.filename,

        "text_length":
            len(text),

        "topics":
            topics,

        "provider":
            "Gemini",

        "model":
            GEMINI_MODEL,
    }


# ============================================================
# QUIZ GENERATION FROM UPLOADED PDF
#
# POST /quiz
# ============================================================

@app.post("/quiz")
async def generate_quiz(
    file: UploadFile = File(...),

    num_questions: int = Query(
        5,
        ge=1,
        le=20
    )
):

    print()

    print("=" * 60)
    print("📝 EDUMIND AI QUIZ REQUEST")
    print("=" * 60)

    validate_pdf_filename(
        file.filename
    )

    print(
        "📄 File:",
        file.filename
    )

    print(
        "❓ Questions:",
        num_questions
    )

    # --------------------------------------------------------
    # Save PDF
    # --------------------------------------------------------

    file_path = get_safe_upload_path(
        file.filename
    )

    try:

        contents = await file.read()

        if not contents:

            raise HTTPException(
                status_code=400,
                detail="Uploaded PDF is empty."
            )

        with open(
            file_path,
            "wb"
        ) as f:

            f.write(contents)

        print(
            "✅ PDF saved:",
            file_path
        )

    except HTTPException:

        raise

    except Exception as error:

        print(
            "❌ PDF save error:",
            error
        )

        raise HTTPException(
            status_code=500,
            detail=(
                "Failed to save PDF: "
                f"{error}"
            )
        )

    # --------------------------------------------------------
    # Extract PDF text
    # --------------------------------------------------------

    try:

        print(
            "📖 Extracting PDF text..."
        )

        text = extract_text_from_pdf(
            str(file_path)
        )

        if not text or not text.strip():

            raise HTTPException(
                status_code=400,
                detail=(
                    "The PDF contains "
                    "no readable text."
                )
            )

        print(
            "✅ Extracted characters:",
            len(text)
        )

    except HTTPException:

        raise

    except Exception as error:

        print(
            "❌ PDF extraction error:",
            error
        )

        raise HTTPException(
            status_code=500,
            detail=(
                "Failed to extract PDF text: "
                f"{error}"
            )
        )

    # --------------------------------------------------------
    # Generate quiz
    # --------------------------------------------------------

    try:

        print()
        print(
            "🧠 Sending PDF content to Gemini..."
        )

        print(
            "🤖 Model:",
            GEMINI_MODEL
        )

        quiz = create_quiz(
            text,
            num_questions
        )

        print(
            "✅ Quiz generated successfully."
        )

        print(
            "📊 Questions returned:",
            len(quiz)
        )

    except ValueError as error:

        print(
            "❌ Quiz validation error:",
            error
        )

        raise HTTPException(
            status_code=422,
            detail=str(error)
        )

    except Exception as error:

        print(
            "❌ Quiz generation failed:",
            error
        )

        raise HTTPException(
            status_code=500,
            detail=(
                "Quiz generation failed: "
                f"{error}"
            )
        )

    if not quiz:

        raise HTTPException(
            status_code=500,
            detail="Gemini returned an empty quiz."
        )

    return {

        "success":
            True,

        "message":
            "Quiz generated successfully.",

        "filename":
            file.filename,

        "questions":
            quiz,

        "total_questions":
            len(quiz),

        "provider":
            "Gemini",

        "model":
            GEMINI_MODEL,
    }
    


# ============================================================
# API QUIZ GENERATION
#
# POST /api/generate-quiz
# ============================================================

@app.post("/api/generate-quiz")
async def generate_quiz_from_uploaded_file(

    filename: str = Query(
        ...,
        min_length=1
    ),

    number_of_questions: int = Query(
        5,
        ge=1,
        le=20
    ),

    language: str = Query(
        "English",
        min_length=1
    )
):

    print()

    print("=" * 60)
    print("📝 API QUIZ GENERATION REQUEST")
    print("=" * 60)

    print(
        "📄 Filename:",
        filename
    )

    print(
        "❓ Number of questions:",
        number_of_questions
    )
    print(
    "🌐 Language:",
    language
)

    # --------------------------------------------------------
    # Validate filename
    # --------------------------------------------------------

    validate_pdf_filename(
        filename
    )

    # --------------------------------------------------------
    # Get uploaded file
    # --------------------------------------------------------

    file_path = get_safe_upload_path(
        filename
    )

    print(
        "📁 Looking for:",
        file_path
    )

    # --------------------------------------------------------
    # Check file exists
    # --------------------------------------------------------

    if not file_path.exists():

        print(
            "❌ File not found:",
            file_path
        )

        raise HTTPException(
            status_code=404,
            detail=(
                f"Uploaded PDF not found: "
                f"{filename}"
            )
        )

    # --------------------------------------------------------
    # Extract PDF text
    # --------------------------------------------------------

    try:

        print(
            "📖 Extracting PDF text..."
        )

        text = extract_text_from_pdf(
            str(file_path)
        )

        if not text or not text.strip():

            raise HTTPException(
                status_code=400,
                detail=(
                    "No readable text found "
                    "in the uploaded PDF."
                )
            )

        print(
            "✅ Extracted characters:",
            len(text)
        )

    except HTTPException:

        raise

    except Exception as error:

        print(
            "❌ PDF extraction error:",
            error
        )

        raise HTTPException(
            status_code=500,
            detail=(
                "Failed to extract PDF text: "
                f"{error}"
            )
        )

    # --------------------------------------------------------
    # Generate quiz
    # --------------------------------------------------------

    try:

        print()
        print(
            "🧠 Generating quiz using Gemini..."
        )

        print(
            "🤖 Model:",
            GEMINI_MODEL
        )

        quiz = create_quiz(
            text,
            number_of_questions,
            language
        )

        if not quiz:

            raise RuntimeError(
                "Gemini returned an empty quiz."
            )

        print(
            "✅ Quiz generated successfully."
        )

        print(
            "📊 Questions:",
            len(quiz)
        )

    except ValueError as error:

        print(
            "❌ Quiz validation error:",
            error
        )

        raise HTTPException(
            status_code=422,
            detail=str(error)
        )

    except Exception as error:

        print(
            "❌ Quiz generation failed:",
            error
        )

        raise HTTPException(
            status_code=500,
            detail=(
                "Quiz generation failed: "
                f"{error}"
            )
        )

    print("=" * 60)

    return {

        "success":
            True,

        "message":
            "Quiz generated successfully.",

        "filename":
            filename,

        "questions":
            quiz,

        "total_questions":
            len(quiz),

        "provider":
            "Gemini",

        "model":
            GEMINI_MODEL,
    }


# ============================================================
# TEXT QUIZ
# ============================================================

@app.post("/quiz/text")
async def generate_quiz_from_text(

    text: str = Body(...),

    num_questions: int = Query(
        5,
        ge=1,
        le=20
    )
):

    print()

    print("=" * 60)
    print("📝 TEXT QUIZ REQUEST")
    print("=" * 60)

    if not text or not text.strip():

        raise HTTPException(
            status_code=400,
            detail="Text cannot be empty."
        )

    try:

        quiz = create_quiz(
            text,
            num_questions
        )

    except ValueError as error:

        raise HTTPException(
            status_code=422,
            detail=str(error)
        )

    except Exception as error:

        print(
            "❌ Text quiz generation failed:",
            error
        )

        raise HTTPException(
            status_code=500,
            detail=(
                "Quiz generation failed: "
                f"{error}"
            )
        )

    return {

        "success":
            True,

        "questions":
            quiz,

        "total_questions":
            len(quiz),

        "provider":
            "Gemini",

        "model":
            GEMINI_MODEL,
    }


# ============================================================
# TOPIC DETECTION
# ============================================================

@app.post("/topics")
async def get_topics(

    file: UploadFile = File(...)
):

    print()

    print("=" * 60)
    print("🏷️ TOPIC DETECTION")
    print("=" * 60)

    validate_pdf_filename(
        file.filename
    )

    file_path = get_safe_upload_path(
        file.filename
    )

    try:

        contents = await file.read()

        if not contents:

            raise HTTPException(
                status_code=400,
                detail="Uploaded PDF is empty."
            )

        with open(
            file_path,
            "wb"
        ) as f:

            f.write(contents)

        text = extract_text_from_pdf(
            str(file_path)
        )

        if not text or not text.strip():

            raise HTTPException(
                status_code=400,
                detail=(
                    "No readable text "
                    "found in the PDF."
                )
            )

        topics = detect_topics(
            text
        )

        print(
            "✅ Topics detected:",
            topics
        )

        return {

            "success":
                True,

            "topics":
                topics,
        }

    except HTTPException:

        raise

    except Exception as error:

        print(
            "❌ Topic detection failed:",
            error
        )

        raise HTTPException(
            status_code=500,
            detail=(
                "Topic detection failed: "
                f"{error}"
            )
        )


# ============================================================
# API DETECT TOPICS
#
# POST /api/detect-topics
# ============================================================

@app.post("/api/detect-topics")
async def api_detect_topics(

    filename: str
):

    safe_filename = Path(
        filename
    ).name

    file_path = UPLOAD_DIR / safe_filename

    if not file_path.exists():

        raise HTTPException(
            status_code=404,
            detail=f"PDF not found: {safe_filename}"
        )

    try:

        text = extract_text_from_pdf(
            str(file_path)
        )

        if not text or not text.strip():

            raise HTTPException(
                status_code=400,
                detail="No readable text found in the PDF."
            )

        topics = detect_topics(
            text
        )

        return {

            "success":
                True,

            "filename":
                safe_filename,

            "topics":
                topics
        }

    except HTTPException:

        raise

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=(
                f"Topic detection failed: "
                f"{error}"
            )
        )


# ============================================================
# SKILL GAP ANALYSIS
#
# POST /api/skill-gaps
# ============================================================

@app.post("/api/skill-gaps")
async def api_skill_gaps(
    data: dict
):

    try:

        print()

        print("=" * 60)
        print("🧠 SKILL GAP ANALYSIS")
        print("=" * 60)

        questions = data.get(
            "questions",
            []
        )

        if not isinstance(
            questions,
            list
        ):

            raise HTTPException(
                status_code=400,
                detail="Questions must be a list."
            )

        if len(questions) == 0:

            return {

                "success":
                    True,

                "skill_gaps":
                    [],

                "message":
                    "No quiz questions were provided."
            }

        skill_gaps = {}

        for question in questions:

            topic = question.get(
                "topic",
                "General"
            )

            is_correct = question.get(
                "is_correct",
                False
            )

            if topic not in skill_gaps:

                skill_gaps[topic] = {

                    "topic":
                        topic,

                    "total":
                        0,

                    "incorrect":
                        0
                }

            skill_gaps[topic]["total"] += 1

            if not is_correct:

                skill_gaps[topic]["incorrect"] += 1

        result = []

        for topic, item in skill_gaps.items():

            total = item["total"]

            incorrect = item["incorrect"]

            percentage = (
                round(
                    (incorrect / total) * 100,
                    2
                )
                if total > 0
                else 0
            )

            if percentage >= 50:

                level = "High"

            elif percentage >= 25:

                level = "Medium"

            else:

                level = "Low"

            result.append({

                "topic":
                    topic,

                "total_questions":
                    total,

                "incorrect_questions":
                    incorrect,

                "gap_percentage":
                    percentage,

                "gap_level":
                    level
            })

        result.sort(
            key=lambda x: x["gap_percentage"],
            reverse=True
        )

        print(
            "✅ Skill gap analysis completed"
        )

        return {

            "success":
                True,

            "message":
                "Skill gaps analyzed successfully.",

            "skill_gaps":
                result
        }

    except HTTPException:

        raise

    except Exception as error:

        print(
            f"❌ Skill gap error: {error}"
        )

        raise HTTPException(
            status_code=500,
            detail=(
                "Skill gap analysis failed: "
                f"{error}"
            )
        )


# ============================================================
# GEMINI AI TUTOR
# ============================================================

@app.post("/ai-tutor")
async def ai_tutor(

    request: TutorRequest
):

    # --------------------------------------------------------
    # Validate question
    # --------------------------------------------------------

    question = (
        request.question.strip()
    )

    if not question:

        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty."
        )

    # --------------------------------------------------------
    # Clean topic
    # --------------------------------------------------------

    topic = (
        request.topic.strip()
        if request.topic
        else "General"
    )

    # --------------------------------------------------------
    # Clean context
    # --------------------------------------------------------

    context = (
        request.context.strip()
        if request.context
        else ""
    )

    print()

    print("=" * 60)
    print("🤖 GEMINI AI TUTOR REQUEST")
    print("=" * 60)

    print(
        "❓ Question:",
        question
    )

    print(
        "📚 Topic:",
        topic
    )

    print(
        "📄 Context:",
        "Provided"
        if context
        else "Not provided"
    )

    # --------------------------------------------------------
    # Call tutor service
    # --------------------------------------------------------

    try:

        tutor_response = ask_ai_tutor(

            question=question,

            context=context,

            topic=topic,
        )

        # ----------------------------------------------------
        # Validate response
        # ----------------------------------------------------

        if not tutor_response:

            raise RuntimeError(
                "Tutor service returned "
                "an empty response."
            )

        answer = tutor_response.get(
            "answer"
        )

        if not answer:

            raise RuntimeError(
                "Tutor service returned "
                "no answer."
            )

        print(
            "✅ Gemini AI Tutor response generated."
        )

        print("=" * 60)

        return {

            "success":
                True,

            "answer":
                answer,

            "model":
                tutor_response.get(
                    "model",
                    GEMINI_MODEL
                ),

            "provider":
                tutor_response.get(
                    "provider",
                    "Gemini"
                ),
        }

    except ValueError as error:

        print(
            "❌ Tutor validation error:",
            error
        )

        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    except RuntimeError as error:

        error_message = str(error)

        print(
            "❌ Gemini Tutor runtime error:",
            error_message
        )

        lower_error = (
            error_message.lower()
        )

        # ----------------------------------------------------
        # Gemini unavailable
        # ----------------------------------------------------

        if (
            "503" in lower_error
            or
            "unavailable" in lower_error
            or
            "high demand" in lower_error
            or
            "service unavailable" in lower_error
            or
            "temporarily unavailable" in lower_error
        ):

            raise HTTPException(
                status_code=503,
                detail=(
                    "Gemini AI Tutor is temporarily "
                    "unavailable. Please try again."
                )
            )

        # ----------------------------------------------------
        # API key error
        # ----------------------------------------------------

        if (
            "api key" in lower_error
            or
            "api_key" in lower_error
            or
            "authentication" in lower_error
            or
            "unauthorized" in lower_error
        ):

            raise HTTPException(
                status_code=500,
                detail=(
                    "Gemini API configuration error. "
                    "Please check GEMINI_API_KEY "
                    "in backend/.env"
                )
            )

        raise HTTPException(
            status_code=500,
            detail=(
                "AI Tutor failed: "
                f"{error_message}"
            )
        )

    except Exception as error:

        print(
            "❌ AI Tutor unexpected error:",
            error
        )

        raise HTTPException(
            status_code=500,
            detail=(
                "AI Tutor failed: "
                f"{error}"
            )
        )


# ============================================================
# SKILL GAP ANALYSIS
#
# POST /skill-gaps
# ============================================================

@app.post("/skill-gaps")
async def skill_gaps(

    request: SkillGapRequest
):

    if request.total_questions <= 0:

        raise HTTPException(
            status_code=400,
            detail="Invalid total question count."
        )

    if not request.questions:

        raise HTTPException(
            status_code=400,
            detail="No quiz questions supplied."
        )

    print()

    print("=" * 60)
    print("🎯 SKILL GAP ANALYSIS")
    print("=" * 60)

    # --------------------------------------------------------
    # Find incorrect questions
    # --------------------------------------------------------

    incorrect_questions = [

        question

        for question in request.questions

        if not question.is_correct
    ]

    # --------------------------------------------------------
    # Find gap topics
    # --------------------------------------------------------

    gap_topics = []

    for question in incorrect_questions:

        topic = (
            question.topic
            or "General"
        )

        if topic not in gap_topics:

            gap_topics.append(
                topic
            )

    # --------------------------------------------------------
    # Build gaps
    # --------------------------------------------------------

    gaps = []

    for topic in gap_topics:

        gaps.append({

            "topic":
                topic,

            "level":
                "Needs Practice",

            "recommendation":
                (
                    "Review this topic "
                    "and practice more "
                    "questions."
                ),
        })

    # --------------------------------------------------------
    # No gaps
    # --------------------------------------------------------

    if not gaps:

        return {

            "success":
                True,

            "skill_gaps":
                [],

            "message":
                (
                    "Excellent! No major "
                    "skill gaps were detected."
                ),
        }

    return {

        "success":
            True,

        "skill_gaps":
            gaps,

        "message":
            (
                f"{len(gaps)} skill area(s) "
                "need additional practice."
            ),
    }


# ============================================================
# PERSONALIZED LEARNING PATH
# ============================================================

@app.post("/learning-path")
async def learning_path(
    request: LearningPathRequest
):
    if request.total_questions <= 0:
        raise HTTPException(
            status_code=400,
            detail="Invalid total question count."
        )

    if not request.questions:
        raise HTTPException(
            status_code=400,
            detail="No quiz questions supplied."
        )

    print()
    print("=" * 60)
    print("🚀 PERSONALIZED LEARNING PATH")
    print("=" * 60)

    percentage = (
        request.score / request.total_questions
    ) * 100

    topic_stats = {}

    for question in request.questions:
        topic = (
            question.topic.strip()
            if question.topic
            else "General"
        )

        if topic not in topic_stats:
            topic_stats[topic] = {
                "topic": topic,
                "total": 0,
                "correct": 0,
                "incorrect": 0
            }

        topic_stats[topic]["total"] += 1

        if question.is_correct:
            topic_stats[topic]["correct"] += 1
        else:
            topic_stats[topic]["incorrect"] += 1

    topic_performance = []

    for topic, stats in topic_stats.items():
        total = stats["total"]
        correct = stats["correct"]
        incorrect = stats["incorrect"]

        topic_percentage = (
            (correct / total) * 100
            if total > 0
            else 0
        )

        if topic_percentage < 50:
            level = "Needs Improvement"
            priority = "High"
            action = "Review the basic concepts and practice more questions."
        elif topic_percentage < 80:
            level = "Developing"
            priority = "Medium"
            action = "Review important concepts and practice moderate questions."
        else:
            level = "Strong"
            priority = "Low"
            action = "Continue practicing and move toward advanced concepts."

        topic_performance.append({
            "topic": topic,
            "total_questions": total,
            "correct_questions": correct,
            "incorrect_questions": incorrect,
            "percentage": round(topic_percentage, 2),
            "level": level,
            "priority": priority,
            "recommended_action": action
        })

    topic_performance.sort(
        key=lambda item: item["percentage"]
    )

    weak_topics = [
        item["topic"]
        for item in topic_performance
        if item["percentage"] < 50
    ]

    developing_topics = [
        item["topic"]
        for item in topic_performance
        if 50 <= item["percentage"] < 80
    ]

    strong_topics = [
        item["topic"]
        for item in topic_performance
        if item["percentage"] >= 80
    ]

    learning_path = []
    step_number = 1

    for item in topic_performance:
        if item["priority"] == "High":
            learning_path.append({
                "step": step_number,
                "topic": item["topic"],
                "priority": "High",
                "level": item["level"],
                "score_percentage": item["percentage"],
                "action": "Review fundamentals",
                "description": "Relearn the core concepts and practice basic questions."
            })
            step_number += 1

    for item in topic_performance:
        if item["priority"] == "Medium":
            learning_path.append({
                "step": step_number,
                "topic": item["topic"],
                "priority": "Medium",
                "level": item["level"],
                "score_percentage": item["percentage"],
                "action": "Practice and strengthen",
                "description": "Review key concepts and solve additional practice questions."
            })
            step_number += 1

    for item in topic_performance:
        if item["priority"] == "Low":
            learning_path.append({
                "step": step_number,
                "topic": item["topic"],
                "priority": "Low",
                "level": item["level"],
                "score_percentage": item["percentage"],
                "action": "Advance further",
                "description": "Continue practicing and explore advanced concepts."
            })
            step_number += 1

    if weak_topics:
        next_topic = weak_topics[0]
        next_action = "Start by reviewing this weak topic before moving to new concepts."
    elif developing_topics:
        next_topic = developing_topics[0]
        next_action = "Strengthen this developing topic with additional practice."
    elif strong_topics:
        next_topic = strong_topics[0]
        next_action = "Move to advanced practice in this topic."
    else:
        next_topic = "General"
        next_action = "Continue practicing the learned concepts."

    if percentage >= 80:
        recommendation = (
            "Excellent performance. Your fundamentals are strong. "
            "Follow the path toward advanced concepts and challenging practice."
        )
    elif percentage >= 50:
        recommendation = (
            "Good progress. Focus first on weak topics, then strengthen "
            "developing topics before moving to advanced concepts."
        )
    else:
        recommendation = (
            "Your learning path should begin with fundamental concepts. "
            "Focus on weak topics and practice step by step before attempting advanced questions."
        )

    result = {
        "success": True,
        "message": "Personalized learning path created successfully.",
        "score": request.score,
        "total_questions": request.total_questions,
        "percentage": round(percentage, 2),
        "weak_topics": weak_topics,
        "developing_topics": developing_topics,
        "strong_topics": strong_topics,
        "topic_performance": topic_performance,
        "learning_path": learning_path,
        "next_topic": next_topic,
        "next_action": next_action,
        "recommendation": recommendation,
        "provider": "EduMind AI",
        "analysis_type": "Personalized Learning Path"
    }

    print("📊 Overall Score:", round(percentage, 2), "%")
    print("🔴 Weak Topics:", weak_topics)
    print("🟡 Developing Topics:", developing_topics)
    print("🟢 Strong Topics:", strong_topics)
    print("➡️ Next Topic:", next_topic)
    print("✅ Personalized Learning Path generated.")
    print("=" * 60)

    return result


# ============================================================
# API LEARNING PATH
#
# POST /api/learning-path
# ============================================================

@app.post("/api/learning-path")
async def api_learning_path(
    request: LearningPathRequest
):
    return await learning_path(request)


# ============================================================
# RECOVERY MODE
# ============================================================

@app.post("/api/recovery-mode")
async def recovery_mode(data: dict):
    try:
        questions = data.get("questions", [])

        if not isinstance(questions, list):
            raise HTTPException(
                status_code=400,
                detail="Questions must be a list."
            )

        if len(questions) == 0:
            raise HTTPException(
                status_code=400,
                detail="No questions supplied."
            )

        print()
        print("=" * 60)
        print("🔄 RECOVERY MODE")
        print("=" * 60)

        weak_questions = [
            question
            for question in questions
            if not bool(question.get("is_correct", False))
        ]

        if len(weak_questions) == 0:
            return {
                "success": True,
                "message": "No recovery required. Excellent performance.",
                "recovery_required": False,
                "weak_question_count": 0,
                "weak_topics": [],
                "recovery_plan": [],
                "provider": "EduMind AI",
                "analysis_type": "Recovery Mode"
            }

        weak_topics = []

        for question in weak_questions:
            topic = str(question.get("topic", "General")).strip()
            if topic and topic not in weak_topics:
                weak_topics.append(topic)

        recovery_plan = []

        for index, question in enumerate(weak_questions):
            recovery_plan.append({
                "recovery_number": index + 1,
                "question": question.get("question", ""),
                "topic": question.get("topic", "General"),
                "student_answer": question.get("student_answer", ""),
                "correct_answer": question.get("correct_answer", ""),
                "reason": "Previous answer was incorrect.",
                "action": "Review the concept and practice a similar question.",
                "priority": "High" if index < 2 else "Medium"
            })

        if len(weak_questions) >= 3:
            recommendation = (
                "Multiple concept gaps were detected. Focus on the weak topics "
                "before attempting another full quiz."
            )
        else:
            recommendation = (
                "A few concept gaps were detected. Review the weak topics and "
                "practice similar questions before retrying."
            )

        print("❌ Weak Questions:", len(weak_questions))
        print("📚 Weak Topics:", weak_topics)
        print("🔄 Recovery Required: Yes")
        print("=" * 60)

        return {
            "success": True,
            "message": "Recovery mode generated successfully.",
            "recovery_required": True,
            "weak_question_count": len(weak_questions),
            "weak_topics": weak_topics,
            "recovery_plan": recovery_plan,
            "recommendation": recommendation,
            "provider": "EduMind AI",
            "analysis_type": "Recovery Mode"
        }

    except HTTPException:
        raise
    except Exception as error:
        print("❌ Recovery Mode Error:", error)
        raise HTTPException(
            status_code=500,
            detail=f"Recovery mode failed: {error}"
        )


# ============================================================
# CONFUSION DETECTOR
#
# POST /api/confusion-detector
# ============================================================

@app.post("/api/confusion-detector")
async def confusion_detector(
    data: dict
):

    try:

        question = str(
            data.get("question", "")
        ).strip()

        correct_answer = str(
            data.get("correct_answer", "")
        ).strip()

        student_answer = str(
            data.get("student_answer", "")
        ).strip()

        explanation = str(
            data.get("explanation", "")
        ).strip()

        topic = str(
            data.get("topic", "General")
        ).strip()

        # ----------------------------------------------------
        # Validation
        # ----------------------------------------------------

        if not question:

            raise HTTPException(
                status_code=400,
                detail="Question is required."
            )

        if not correct_answer:

            raise HTTPException(
                status_code=400,
                detail="Correct answer is required."
            )

        if not student_answer:

            raise HTTPException(
                status_code=400,
                detail="Student answer is required."
            )

        # ----------------------------------------------------
        # Analysis
        # ----------------------------------------------------

        print()
        print("=" * 60)
        print("🧠 CONFUSION DETECTOR")
        print("=" * 60)

        print(
            "📚 Topic:",
            topic
        )

        print(
            "❓ Question:",
            question
        )

        print(
            "👤 Student answer:",
            student_answer
        )

        print(
            "💭 Explanation:",
            explanation
        )

        result = analyze_confusion(

            question=question,

            correct_answer=correct_answer,

            student_answer=student_answer,

            explanation=explanation,

            topic=topic

        )

        print(
            "📊 Understanding:",
            result.get(
                "understanding_score",
                0
            )
        )

        print(
            "⚠️ Confusion:",
            result.get(
                "confusion_level",
                "Unknown"
            )
        )

        print("=" * 60)

        return result

    except HTTPException:
        raise

    except Exception as error:

        print(
            "❌ Confusion Detector error:",
            error
        )

        raise HTTPException(
            status_code=500,
            detail=(
                "Confusion analysis failed: "
                f"{error}"
            )
        )

# ============================================================
# QUESTION INTELLIGENCE
#
# POST /api/question-intelligence
# ============================================================

@app.post("/api/question-intelligence")
async def question_intelligence(data: dict):
    try:
        questions = data.get("questions", [])

        if not isinstance(questions, list):
            raise HTTPException(status_code=400, detail="Questions must be a list.")

        if len(questions) == 0:
            raise HTTPException(status_code=400, detail="No questions supplied.")

        print()
        print("=" * 60)
        print("📄 QUESTION INTELLIGENCE")
        print("=" * 60)

        analyzed_questions = []

        for index, question in enumerate(questions):
            question_text = str(question.get("question", "")).strip()
            topic = str(question.get("topic", "General")).strip()
            time_spent = float(question.get("time_spent", 0) or 0)
            is_correct = bool(question.get("is_correct", False))

            if time_spent >= 60:
                difficulty = "Challenging"
            elif time_spent >= 30:
                difficulty = "Moderate"
            else:
                difficulty = "Easy"

            if is_correct and time_spent < 30:
                performance = "Strong"
                insight = "Student answered quickly and correctly."
            elif is_correct and time_spent >= 30:
                performance = "Understood"
                insight = "Student understood the question but required additional thinking time."
            elif not is_correct and time_spent < 30:
                performance = "Concept Gap"
                insight = "Student answered quickly but the answer was incorrect. The concept may need review."
            else:
                performance = "Needs Practice"
                insight = "Student spent significant time and still answered incorrectly. Additional practice is recommended."

            analyzed_questions.append({
                "question_number": index + 1,
                "question": question_text,
                "topic": topic,
                "time_spent": round(time_spent, 2),
                "is_correct": is_correct,
                "difficulty": difficulty,
                "performance": performance,
                "insight": insight
            })

        total_questions = len(analyzed_questions)
        correct_questions = sum(1 for item in analyzed_questions if item["is_correct"])
        incorrect_questions = total_questions - correct_questions
        total_time = sum(item["time_spent"] for item in analyzed_questions)
        average_time = total_time / total_questions if total_questions > 0 else 0
        most_difficult_question = max(analyzed_questions, key=lambda item: item["time_spent"])
        strong_questions = [item for item in analyzed_questions if item["performance"] == "Strong"]

        if incorrect_questions == 0:
            overall_insight = "Excellent performance. The student answered all questions correctly."
        elif correct_questions >= total_questions * 0.6:
            overall_insight = "Good performance with some areas requiring additional practice."
        else:
            overall_insight = "Several questions indicate concept gaps and require focused review."

        print("📊 Total Questions:", total_questions)
        print("✅ Correct:", correct_questions)
        print("❌ Incorrect:", incorrect_questions)
        print("⏱️ Average Time:", round(average_time, 2), "seconds")
        print("🎯 Most Time-Consuming Question:", most_difficult_question["question_number"])
        print("=" * 60)

        return {
            "success": True,
            "message": "Question intelligence generated successfully.",
            "total_questions": total_questions,
            "correct_questions": correct_questions,
            "incorrect_questions": incorrect_questions,
            "average_time": round(average_time, 2),
            "most_time_consuming_question": most_difficult_question,
            "strong_questions": len(strong_questions),
            "overall_insight": overall_insight,
            "questions": analyzed_questions,
            "provider": "EduMind AI",
            "analysis_type": "Question Intelligence"
        }

    except HTTPException:
        raise
    except Exception as error:
        print("❌ Question Intelligence Error:", error)
        raise HTTPException(
            status_code=500,
            detail=f"Question intelligence analysis failed: {error}"
        )

# ============================================================
# EXPLAIN-TO-LEARN AI
# GEMINI POWERED
#
# POST /api/explain-to-learn
# ============================================================

@app.post("/api/explain-to-learn")
async def explain_to_learn(data: dict):
    try:
        question = str(data.get("question", "")).strip()
        topic = str(data.get("topic", "General")).strip()
        student_answer = str(data.get("student_answer", "")).strip()
        correct_answer = str(data.get("correct_answer", "")).strip()

        if not question:
            raise HTTPException(status_code=400, detail="Question is required.")
        if not correct_answer:
            raise HTTPException(status_code=400, detail="Correct answer is required.")

        print()
        print("=" * 60)
        print("🧠 GEMINI EXPLAIN-TO-LEARN AI")
        print("=" * 60)
        print("📚 Topic:", topic)
        print("❓ Question:", question)
        print("👤 Student Answer:", student_answer)
        print("✅ Correct Answer:", correct_answer)

        if not GEMINI_API_KEY:
            raise HTTPException(status_code=500, detail="Gemini API key is not configured.")

        client = genai.Client(api_key=GEMINI_API_KEY)

        prompt = f"""
You are EduMind AI, an intelligent personalized learning assistant for students.

Analyze the student's answer and teach the concept clearly.

IMPORTANT:
- Do not simply repeat the correct answer.
- Explain why the student's answer is wrong.
- Explain the underlying concept in simple student-friendly language.
- Use the question and topic as context.
- Give a practical real-world example.
- Give a short memory tip.
- Give one simple follow-up practice question.
- Keep the explanation educational and concise.
- Do not insult or discourage the student.
- If the student's answer is partially correct, clearly explain what part is correct and what part needs improvement.

Return ONLY valid JSON.

Use exactly this structure:
{{
    "why_student_wrong": "...",
    "explanation": "...",
    "example": "...",
    "memory_tip": "...",
    "next_step": "...",
    "practice_question": "..."
}}

Topic:
{topic}

Question:
{question}

Student Answer:
{student_answer}

Correct Answer:
{correct_answer}
"""

        print("🧠 Sending Explain-to-Learn request to Gemini...")
        print("🤖 Model:", GEMINI_MODEL)

        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt
        )

        if not response or not response.text:
            raise RuntimeError("Gemini returned an empty response.")

        raw_response = response.text.strip()

        if raw_response.startswith("```json"):
            raw_response = raw_response.replace("```json", "", 1).replace("```", "").strip()
        elif raw_response.startswith("```"):
            raw_response = raw_response.replace("```", "").strip()

        try:
            result = json.loads(raw_response)
        except json.JSONDecodeError as error:
            print("❌ Gemini JSON parsing error:", error)
            print("📦 Raw Gemini response:", raw_response)
            raise RuntimeError("Gemini returned an invalid Explain-to-Learn response.")

        why_student_wrong = str(result.get("why_student_wrong", "")).strip()
        explanation = str(result.get("explanation", "")).strip()
        example = str(result.get("example", "")).strip()
        memory_tip = str(result.get("memory_tip", "")).strip()
        next_step = str(result.get("next_step", "")).strip()
        practice_question = str(result.get("practice_question", "")).strip()

        if not explanation:
            raise RuntimeError("Gemini did not generate an explanation.")

        print("✅ Personalized explanation generated.")
        print("=" * 60)

        return {
            "success": True,
            "question": question,
            "topic": topic,
            "student_answer": student_answer,
            "correct_answer": correct_answer,
            "why_student_wrong": why_student_wrong,
            "explanation": explanation,
            "example": example,
            "memory_tip": memory_tip,
            "next_step": next_step,
            "practice_question": practice_question,
            "provider": "Gemini",
            "model": GEMINI_MODEL,
            "analysis_type": "Explain-to-Learn AI"
        }

    except HTTPException:
        raise
    except Exception as error:
        print("❌ Explain-to-Learn Gemini Error:", error)
        raise HTTPException(
            status_code=500,
            detail=f"Explain-to-Learn failed: {error}"
        )


# ============================================================
# RUN SERVER
# ============================================================

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
    )
