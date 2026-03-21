import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from google import genai
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()

# ✅ Use absolute path to frontend
frontend_path = os.path.join(os.path.dirname(__file__), "..", "frontend")
frontend_path = os.path.abspath(frontend_path)

if not os.path.isdir(frontend_path):
    print("⚠️ Frontend folder not found:", frontend_path)

app.mount("/static", StaticFiles(directory=frontend_path), name="static")

# ✅ Correct way to initialize client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

@app.get("/")
def serve_frontend():
    return FileResponse(os.path.join(frontend_path, "index.html"))

@app.get("/generate")
def generate_code(prompt: str):
    try:
        response = client.models.generate_content(
    model="models/gemini-1.5-flash",  # ✅ include the full path
    contents=prompt
)

        return {"result": response.text}
    except Exception as e:
        return {"error": f"Generation failed: {str(e)}"}
