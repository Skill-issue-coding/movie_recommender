from dotenv import load_dotenv
from google import genai
import os

# load api key from .env
load_dotenv()

if os.getenv("GOOGLE_API_KEY"):
    print("✅ GOOGLE_API_KEY successfully loaded from .env.")
else:
    print("❌ Error: GOOGLE_API_KEY not found. Check your .env file.")
    exit()

try:
    client = genai.Client()

    test_prompt="What are the three most famous historical periods of filmmaking?"

    response = client.models.generate_content(
        model="gemini-2.5-flash", contents=test_prompt
    )

    print("\n--- Response ---")
    print(response.text)
    print("\n--- Test Complete ---")

except Exception as e:
    print(f"❌ Gemini API Call Failed: {e}")
