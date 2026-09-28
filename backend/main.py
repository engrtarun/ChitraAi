from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from groq import AsyncGroq
import google.generativeai as genai

from config import GROQ_API_KEY, GEMINI_API_KEY

app = FastAPI(title="ChitraAi Chat Backend Fallback API")

# Define API Contract for LobeChat / Frontend
# Frontend tries Puter.js first in the browser. 
# If Puter fails, it calls THIS endpoint.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, restrict this to frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str

# Initialize fallback clients if keys are available
groq_client = AsyncGroq(api_key=GROQ_API_KEY) if GROQ_API_KEY and GROQ_API_KEY != "your_groq_api_key_here" else None

if GEMINI_API_KEY and GEMINI_API_KEY != "your_gemini_api_key_here":
    genai.configure(api_key=GEMINI_API_KEY)
    gemini_model = genai.GenerativeModel('gemini-2.5-flash')
else:
    gemini_model = None

async def call_groq(prompt: str) -> str:
    if not groq_client:
        raise ValueError("Groq API key not configured")
    
    chat_completion = await groq_client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="llama3-8b-8192", 
    )
    return chat_completion.choices[0].message.content

async def call_gemini(prompt: str) -> str:
    if not gemini_model:
        raise ValueError("Gemini API key not configured")
    
    response = await gemini_model.generate_content_async(prompt)
    return response.text

@app.post("/api/chat")
async def chat_endpoint(request: ChatRequest):
    """
    Fallback Chat API for the Frontend.
    Frontend should call Puter.js directly first. If rate-limited, call this.
    """
    prompt = request.message
    
    # 1. Try Groq (Primary Fallback)
    try:
        response_text = await call_groq(prompt)
        return {"provider": "groq", "response": response_text}
    except Exception as e:
        print(f"Groq failed: {e}")
        pass
        
    # 2. Try Gemini (Secondary Fallback)
    try:
        response_text = await call_gemini(prompt)
        return {"provider": "gemini", "response": response_text}
    except Exception as e:
        print(f"Gemini failed: {e}")
        raise HTTPException(status_code=500, detail="All Fallback AI providers (Groq/Gemini) failed.")

@app.get("/")
def read_root():
    return {"status": "ok", "message": "ChitraAi Fallback Backend is running"}
