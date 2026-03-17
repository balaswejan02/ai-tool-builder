from fastapi import FastAPI
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from google import genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize FastAPI
app = FastAPI()

# Mount frontend folder as static
app.mount("/static", StaticFiles(directory="../frontend"), name="static")

# Gemini client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# Request schema
class ToolIdea(BaseModel):
    idea: str

@app.get("/")
async def serve_frontend():
    return FileResponse("../frontend/index.html")

@app.post("/build")
async def build_tool(idea: ToolIdea):
    try:
        response = client.models.generate_content(
            model="models/gemini-2.5-flash",   # fast model
            contents=f"Generate Python code for: {idea.idea}"
        )
        code = response.text.strip() if response.text else "# No code generated."
        return JSONResponse({"code": code})
    except Exception as e:
        return JSONResponse({"error": str(e)})
