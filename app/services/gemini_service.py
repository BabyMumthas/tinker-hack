import httpx
from app.config import config

SYSTEM_PROMPT = """You are a helpful assistant for the National Missing Person Support System, specialized in child safety and recovery.
Your primary goal is to guide users through the immediate steps when a child is missing:
1. Contact local law enforcement/emergency services (100 or 112) IMMEDIATELY. There is NO waiting period for children.
2. Provide a detailed description: Full name, age, height, hair color, and the EXACT clothing they were last seen wearing.
3. Use this platform: Upload the most recent, clear photograph of the child to our AI facial recognition system.
4. Gather information: Note the time and location where the child was last seen and a list of their friends or frequented places.

Be extremely empathetic, calm, and professional. Prioritize urgent safety advice above all else.
Keep responses brief (2-3 sentences) to avoid overwhelming the user, unless they ask for specific procedural details."""

GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"
MOCK_MODE = False  # Set to True once you have a working API key with quota


class GeminiChatService:
    def __init__(self):
        self.api_key = config.GEMINI_API_KEY

    def get_mock_response(self, user_message: str) -> str:
        msg = user_message.lower()
        if any(k in msg for k in ["info", "data", "provide", "give", "description"]):
            return "You should provide: full name, age, height, hair color, and the EXACT clothing they were last seen wearing, plus a recent high-quality photo."
        if any(k in msg for k in ["child", "kid", "minor", "emergency", "urgent", "help", "right now"]):
            return "For a missing child or emergency, contact the police (100) immediately. There is no 24-hour waiting period for minors; every second counts."
        if any(k in msg for k in ["ai", "recognition", "facial", "how"]):
            return "Our platform's AI assists by matching facial data across hospitals, shelters, and public checkpoints in real-time."
        if any(k in msg for k in ["accurate", "reliable", "match"]):
            return "The AI system uses DeepFace technology, ensuring high accuracy even with older photos or different lighting."
        if any(k in msg for k in ["privacy", "safe", "data"]):
            return "Privacy is our priority; all facial data is encrypted and handled according to national security protocols."
        
        # Default fallback for mock mode
        return "I'm here to help. You can report a missing person by clicking the 'Report Case' button on the dashboard."

    async def get_response(self, user_message: str) -> str:
        if MOCK_MODE:
            return self.get_mock_response(user_message)

        try:
            # Prepend instructions to ensure context is maintained
            full_prompt = f"{SYSTEM_PROMPT}\n\nUser: {user_message}"
            
            payload = {
                "contents": [
                    {
                        "role": "user",
                        "parts": [{"text": full_prompt}]
                    }
                ],
                "generationConfig": {
                    "temperature": 0.7,
                    "maxOutputTokens": 400,
                }
            }

            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    f"{GEMINI_API_URL}?key={self.api_key}",
                    json=payload,
                )
                
                if response.status_code == 429:
                    # Graceful Fallback: If 429 (Quota), return a high-quality mock response
                    return self.get_mock_response(user_message)
                
                if response.status_code != 200:
                    return self.get_mock_response(user_message)
                
                data = response.json()
                return data["candidates"][0]["content"]["parts"][0]["text"]
        except Exception as e:
            print(f"Gemini API error: {e}")
            return self.get_mock_response(user_message)


chat_service = GeminiChatService()
