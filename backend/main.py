import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import google.genai as genai

from dotenv import load_dotenv

load_dotenv()
app = FastAPI()

# ✅ Use absolute path to frontend
frontend_path = os.path.join(os.path.dirname(__file__), "..", "frontend")
frontend_path = os.path.abspath(frontend_path)

if not os.path.isdir(frontend_path):
    print("⚠️ Frontend folder not found:", frontend_path)

app.mount("/static", StaticFiles(directory=frontend_path), name="static")

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

@app.get("/")
def serve_frontend():
    return FileResponse(os.path.join(frontend_path, "index.html"))

@app.get("/generate")
def generate_code(prompt: str):
    response = model.generate_content(prompt)
    return {"result": response.text}
