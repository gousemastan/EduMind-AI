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

if not GEMINI_API_KEY:
    raise RuntimeError(
        "GEMINI_API_KEY is not configured."
    )

client = genai.Client(
    api_key=GEMINI_API_KEY
)


# ============================================================
# GEMINI QUOTA ERROR CHECK
# ============================================================

def is_quota_error(error):
    message = str(error).lower()

    return (
        "429" in message
        or "resource_exhausted" in message
        or "resource exhausted" in message
        or "quota exceeded" in message
        or "generaterequestsperdayperproject-freetier" in message
    )


# ============================================================
# LOCAL FALLBACK FLASHCARDS
# ============================================================

def generate_local_fallback_flashcards(
    text: str,
    num_cards: int = 10
):
    """
    Creates basic flashcards locally when
    Gemini quota is unavailable.
    """

    if not text or not text.strip():
        raise ValueError(
            "No text available for flashcard generation."
        )

    clean_text = re.sub(
        r"\s+",
        " ",
        text
    ).strip()

    sentences = re.split(
        r"(?<=[.!?])\s+",
        clean_text
    )

    sentences = [
        sentence.strip()
        for sentence in sentences
        if sentence.strip()
    ]

    cards = []

    # --------------------------------------------------------
    # Use definitions / colon-based statements first
    # --------------------------------------------------------

    for sentence in sentences:

        if ":" in sentence:

            parts = sentence.split(":", 1)

            question_part = parts[0].strip()
            answer_part = parts[1].strip()

            if question_part and answer_part:

                cards.append({
                    "question": (
                        f"What is {question_part}?"
                    ),
                    "answer": answer_part
                })

        if len(cards) >= num_cards:
            break

    # --------------------------------------------------------
    # Use normal sentences if not enough cards
    # --------------------------------------------------------

    if len(cards) < num_cards:

        for sentence in sentences:

            if sentence in [
                card["answer"]
                for card in cards
            ]:
                continue

            cards.append({
                "question": (
                    "What important information is "
                    "described in this statement?"
                ),
                "answer": sentence
            })

            if len(cards) >= num_cards:
                break

    # --------------------------------------------------------
    # Final fallback if PDF contains very little text
    # --------------------------------------------------------

    if not cards:

        cards.append({
            "question": "What is the main study material?",
            "answer": clean_text[:1000]
        })

    return cards[:num_cards]


# ============================================================
# GEMINI FLASHCARD GENERATION
# ============================================================

def generate_flashcards(
    text: str,
    num_cards: int = 10
):

    if not text or not text.strip():
        raise ValueError(
            "No text available for flashcard generation."
        )

    try:

        prompt = f"""
You are an AI study assistant.

Create {num_cards} useful study flashcards
from the following study material.

RULES:

1. Focus only on important concepts.
2. Questions must be clear and useful for exam preparation.
3. Answers must be short but complete.
4. Avoid duplicate questions.
5. Do not invent information outside the provided material.
6. Return ONLY valid JSON.
7. Use exactly this structure:

{{
  "flashcards": [
    {{
      "question": "Question here",
      "answer": "Answer here"
    }}
  ]
}}

STUDY MATERIAL:

{text}
"""

        print()
        print("=" * 60)
        print("🧠 GEMINI FLASHCARD GENERATION")
        print("=" * 60)
        print(f"🤖 Model: {GEMINI_MODEL}")
        print(f"📊 Requested cards: {num_cards}")
        print("📡 Sending request to Gemini...")

        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt
        )

        raw_text = getattr(
            response,
            "text",
            None
        )

        if not raw_text:
            raise ValueError(
                "Gemini returned an empty response."
            )

        raw_text = raw_text.strip()

        # ----------------------------------------------------
        # Remove Markdown JSON fences
        # ----------------------------------------------------

        raw_text = re.sub(
            r"^```json\s*",
            "",
            raw_text,
            flags=re.IGNORECASE
        )

        raw_text = re.sub(
            r"^```\s*",
            "",
            raw_text
        )

        raw_text = re.sub(
            r"\s*```$",
            "",
            raw_text
        )

        # ----------------------------------------------------
        # Parse JSON
        # ----------------------------------------------------

        data = json.loads(raw_text)

        if "flashcards" not in data:
            raise ValueError(
                "Gemini response does not contain flashcards."
            )

        flashcards = data["flashcards"]

        if not isinstance(
            flashcards,
            list
        ):
            raise ValueError(
                "Invalid flashcards format."
            )

        cleaned_cards = []

        for card in flashcards:

            if not isinstance(
                card,
                dict
            ):
                continue

            question = str(
                card.get(
                    "question",
                    ""
                )
            ).strip()

            answer = str(
                card.get(
                    "answer",
                    ""
                )
            ).strip()

            if question and answer:

                cleaned_cards.append({
                    "question": question,
                    "answer": answer
                })

        if not cleaned_cards:
            raise ValueError(
                "No valid flashcards were generated."
            )

        print(
            f"✅ Gemini generated {len(cleaned_cards)} flashcards."
        )

        return cleaned_cards[:num_cards]

    # ========================================================
    # GEMINI QUOTA → LOCAL FALLBACK
    # ========================================================

    except Exception as error:

        if is_quota_error(error):

            print()
            print(
                "⚠️ Gemini flashcard quota exhausted."
            )

            print(
                "🔄 Switching to local fallback flashcards..."
            )

            fallback_cards = (
                generate_local_fallback_flashcards(
                    text,
                    num_cards
                )
            )

            print(
                f"✅ Local fallback generated "
                f"{len(fallback_cards)} flashcards."
            )

            return fallback_cards

        # ----------------------------------------------------
        # Other errors
        # ----------------------------------------------------

        print(
            f"❌ Flashcard Generation Error: {error}"
        )

        raise