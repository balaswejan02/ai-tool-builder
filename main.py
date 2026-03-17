import os
import requests
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from dotenv import load_dotenv
import os

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

class ToolIdea(BaseModel):
    idea: str

@app.post("/build")
async def build_tool(idea: ToolIdea):
    try:
        response = requests.post(
            "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-pro:generateContent",
            headers={"Authorization": f"Bearer {GEMINI_API_KEY}"},
            json={
                "contents": [
                    {"parts": [{"text": f"Generate Python code for: {idea.idea}"}]}
                ]
            }
        )
        data = response.json()

        code = (
            data.get("candidates", [{}])[0]
            .get("content", {})
            .get("parts", [{}])[0]
            .get("text", "")
        )

        if not code:
            code = "# No code generated. Check API key or request."

        return JSONResponse({"code": code})

    except Exception as e:
        return JSONResponse({"error": str(e)})
