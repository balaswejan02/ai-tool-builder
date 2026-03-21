import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from google import genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI()

# ✅ Frontend path setup
frontend_path = os.path.join(os.path.dirname(__file__), "..", "frontend")
frontend_path = os.path.abspath(frontend_path)

if not os.path.isdir(frontend_path):
    print("⚠️ Frontend folder not found:", frontend_path)

app.mount("/static", StaticFiles(directory=frontend_path), name="static")

# ✅ Initialize client with API key
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

@app.get("/")
def serve_frontend():
    return FileResponse(os.path.join(frontend_path, "index.html"))

# ✅ Route to list available models
@app.get("/models")
def list_models():
    try:
        models = client.models.list()
        return {"models": [m.name for m in models]}
    except Exception as e:
        return {"error": str(e)}

# ✅ Generate endpoint with safe fallback
@app.get("/models")
def list_models():
    try:
        models = client.models.list()
        return {"models": [m.name for m in models]}
    except Exception as e:
        return {"error": str(e)}
