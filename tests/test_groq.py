import asyncio
import os
from groq import AsyncGroq
from dotenv import load_dotenv

load_dotenv(dotenv_path="../.env")

async def test_groq():
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key or api_key == "your_groq_api_key_here":
        print("❌ Groq API key not found in .env")
        return

    print("Testing Groq API...")
    try:
        client = AsyncGroq(api_key=api_key)
        response = await client.chat.completions.create(
            messages=[{"role": "user", "content": "Hello, answer in 5 words."}],
            model="llama3-8b-8192",
        )
        print("✅ Groq Test Success:", response.choices[0].message.content)
    except Exception as e:
        print("❌ Groq Test Failed:", e)

if __name__ == "__main__":
    asyncio.run(test_groq())
