# parser.py (Optimized API call using Structured Outputs)
import os
import json
from google import genai
from google.genai import types # Import types for structured schema
from models import Transaction

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

def parse_sms_ai(sms_text: str):
    prompt = f"Extract financial data from this Indian banking SMS: {sms_text}"
    
    try:
        # Enforce JSON output matching our Pydantic model directly at the API boundary
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=Transaction,
            ),
        )
        
        # response.text is now guaranteed to be clean valid JSON matching your schema
        data = json.loads(response.text)
        return data

    except Exception as e:
        print("❌ PARSING ERROR:", e)
        return {
            "amount": None,
            "merchant": "UNKNOWN",
            "bank_name": "UNKNOWN",
            "type": "UNKNOWN",
            "category": "Other",
            "plain_language_summary": "Couldn't translate transaction text automatically."
        }