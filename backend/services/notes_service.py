import os
import re
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


# =========================================================
# GEMINI CLIENT
# =========================================================

def get_gemini_client():
    global _client

    if _client is not None:
        return _client

    if not GEMINI_API_KEY:
        raise RuntimeError("GEMINI_API_KEY is missing.")

    _client = genai.Client(
        api_key=GEMINI_API_KEY
    )

    return _client


# =========================================================
# JSON EXTRACTOR
# =========================================================

def extract_json(text):
    text = text.strip()

    text = re.sub(
        r"^```json\s*",
        "",
        text,
        flags=re.IGNORECASE
    )

    text = re.sub(
        r"\s*```$",
        "",
        text
    )

    try:
        return json.loads(text)
    except Exception:
        pass

    start = text.find("{")
    end = text.rfind("}")

    if start != -1 and end != -1:
        return json.loads(
            text[start:end + 1]
        )

    raise ValueError(
        "Invalid JSON returned by Gemini."
    )


# =========================================================
# QUOTA ERROR CHECK
# =========================================================

def is_quota_error(error):
    message = str(error).lower()

    return (
        "429" in message
        or "resource_exhausted" in message
        or "resource exhausted" in message
        or "quota exceeded" in message
        or "generaterequestsperdayperproject-freetier" in message
    )


# =========================================================
# LOCAL FALLBACK NOTES
# =========================================================

def generate_local_fallback_notes(
    text: str,
    language: str = "English"
):
    """
    Creates basic study notes locally when
    Gemini quota is unavailable.
    """

    if not text or not text.strip():
        raise ValueError(
            "Source text cannot be empty."
        )

    # Clean extracted PDF text
    clean_text = re.sub(
        r"\s+",
        " ",
        text
    ).strip()

    # Split into sentences
    sentences = re.split(
        r"(?<=[.!?])\s+",
        clean_text
    )

    sentences = [
        sentence.strip()
        for sentence in sentences
        if sentence.strip()
    ]

    # Limit text used for fallback
    useful_sentences = sentences[:15]

    # -----------------------------------------------------
    # English
    # -----------------------------------------------------

    if language == "English":

        summary = (
            "These study notes summarize the main information "
            "available in the uploaded learning material."
        )

        key_points = useful_sentences[:7]

        definitions = []

        for sentence in useful_sentences:
            if ":" in sentence:
                parts = sentence.split(":", 1)

                term = parts[0].strip()
                definition = parts[1].strip()

                if term and definition:
                    definitions.append({
                        "term": term[:100],
                        "definition": definition[:300]
                    })

            if len(definitions) >= 5:
                break

        notes = []

        for index, sentence in enumerate(
            useful_sentences[:8],
            start=1
        ):
            notes.append({
                "heading": f"Important Point {index}",
                "content": sentence
            })

        if not notes:
            notes.append({
                "heading": "Study Material",
                "content": clean_text[:1000]
            })

        return {
            "title": "Study Notes",
            "summary": summary,
            "key_points": key_points,
            "definitions": definitions,
            "notes": notes
        }

    # -----------------------------------------------------
    # Telugu
    # -----------------------------------------------------

    if language == "Telugu":

        key_points = useful_sentences[:7]

        notes = []

        for index, sentence in enumerate(
            useful_sentences[:8],
            start=1
        ):
            notes.append({
                "heading": f"ముఖ్యమైన అంశం {index}",
                "content": sentence
            })

        return {
            "title": "అధ్యయన నోట్స్",
            "summary": (
                "అప్‌లోడ్ చేసిన విద్యా విషయాల నుండి "
                "ముఖ్యమైన అంశాలను ఈ నోట్స్‌లో చూపించాం."
            ),
            "key_points": key_points,
            "definitions": [],
            "notes": notes
        }

    # -----------------------------------------------------
    # Hindi
    # -----------------------------------------------------

    if language == "Hindi":

        key_points = useful_sentences[:7]

        notes = []

        for index, sentence in enumerate(
            useful_sentences[:8],
            start=1
        ):
            notes.append({
                "heading": f"महत्वपूर्ण बिंदु {index}",
                "content": sentence
            })

        return {
            "title": "अध्ययन नोट्स",
            "summary": (
                "अपलोड की गई अध्ययन सामग्री से "
                "मुख्य जानकारी इन नोट्स में दी गई है।"
            ),
            "key_points": key_points,
            "definitions": [],
            "notes": notes
        }

    # -----------------------------------------------------
    # Other languages
    # -----------------------------------------------------

    key_points = useful_sentences[:7]

    notes = []

    for index, sentence in enumerate(
        useful_sentences[:8],
        start=1
    ):
        notes.append({
            "heading": f"Important Point {index}",
            "content": sentence
        })

    return {
        "title": "Study Notes",
        "summary": (
            "Study notes generated from the uploaded material."
        ),
        "key_points": key_points,
        "definitions": [],
        "notes": notes
    }


# =========================================================
# AI NOTES
# =========================================================

def generate_ai_notes(
    text: str,
    language: str = "English"
):

    if not text or not text.strip():
        raise ValueError(
            "Source text cannot be empty."
        )

    try:

        client = get_gemini_client()

        prompt = f"""
You are EduMind AI, an expert educational assistant.

Create clear study notes from the supplied learning material.

LANGUAGE REQUIREMENT:

Generate the entire study notes in {language}.

The title, summary, key points, definitions,
headings, and explanations must all be written
in {language}.

IMPORTANT RULES:

1. Use ONLY information from the supplied material.
2. Do not invent facts.
3. Make the notes easy for a diploma/college student to understand.
4. Create a short summary.
5. Create important key points.
6. Create important definitions when they exist.
7. Organize the notes using headings.
8. Keep the notes exam-friendly.
9. Return ONLY valid JSON.
10. Do not use Markdown code fences.

Required JSON structure:

{{
    "title": "Study Notes",
    "summary": "Short summary of the material",
    "key_points": [
        "Important point 1",
        "Important point 2",
        "Important point 3"
    ],
    "definitions": [
        {{
            "term": "Term",
            "definition": "Definition"
        }}
    ],
    "notes": [
        {{
            "heading": "Topic heading",
            "content": "Clear explanation"
        }}
    ]
}}

LEARNING MATERIAL:

{text}
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
                "Gemini returned an empty response."
            )

        return extract_json(response_text)

    # =====================================================
    # GEMINI QUOTA → LOCAL FALLBACK
    # =====================================================

    except Exception as error:

        if is_quota_error(error):

            print(
                "⚠️ Gemini notes quota exhausted."
            )

            print(
                "🔄 Switching to local fallback notes..."
            )

            fallback_notes = generate_local_fallback_notes(
                text,
                language
            )

            print(
                "✅ Local fallback notes generated."
            )

            return fallback_notes

        # Other errors should still be reported
        raise