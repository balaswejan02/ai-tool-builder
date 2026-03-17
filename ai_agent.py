import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

print("API KEY:", os.getenv("GEMINI_API_KEY"))

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def build_tool(idea: str):
    prompt = f"""
Create a complete working project for:

{idea}

Include:
- HTML
- CSS
- JavaScript
- Instructions
"""

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",   # ✅ FIXED MODEL
            contents=prompt
        )
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"