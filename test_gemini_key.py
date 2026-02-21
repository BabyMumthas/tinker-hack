import asyncio
import httpx
import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent"

async def test_key():
    if not GEMINI_API_KEY or "your_gemini_api_key_here" in GEMINI_API_KEY:
        print("API Key is missing or is still a placeholder.")
        return

    payload = {
        "contents": [{"role": "user", "parts": [{"text": "Say 'Key works!'"}]}]
    }

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(
                f"{GEMINI_API_URL}?key={GEMINI_API_KEY}",
                json=payload,
            )
            if response.status_code == 200:
                data = response.json()
                print("SUCCESS: Gemini response:", data["candidates"][0]["content"]["parts"][0]["text"])
            else:
                print(f"FAILURE: Status {response.status_code}")
                print(response.text)
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    asyncio.run(test_key())
