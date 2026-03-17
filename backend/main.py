import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI()

# ✅ Correct path to frontend folder
frontend_path = os.path.join(os.path.dirname(__file__), "..", "frontend")
app.mount("/static", StaticFiles(directory=frontend_path), name="static")

# ✅ Gemini API setup
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

# Serve index.html at root
@app.get("/")
def serve_frontend():
    return FileResponse(os.path.join(frontend_path, "index.html"))

# Example API endpoint: generate code from user prompt
@app.get("/generate")
def generate_code(prompt: str):
    response = model.generate_content(prompt)
    return {"result": response.text}
