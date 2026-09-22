import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("❌ GEMINI_API_KEY not found in .env")
    raise SystemExit(1)

print("🔑 Gemini API key found")
print()
print("📋 Available Gemini models:")
print("=" * 60)

try:
    client = genai.Client(api_key=api_key)

    for model in client.models.list():
        print(model.name)

    print("=" * 60)
    print("✅ Model check completed.")

except Exception as error:
    print("=" * 60)
    print("❌ Failed to list Gemini models")
    print(error)