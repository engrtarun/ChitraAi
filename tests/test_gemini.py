import asyncio
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv(dotenv_path="../.env")

async def test_gemini():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key or api_key == "your_gemini_api_key_here":
        print("❌ Gemini API key not found in .env")
        return

    print("Testing Gemini API...")
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.5-flash')
        response = await model.generate_content_async("Hello, answer in 5 words.")
        print("✅ Gemini Test Success:", response.text)
    except Exception as e:
        print("❌ Gemini Test Failed:", e)

if __name__ == "__main__":
    asyncio.run(test_gemini())
