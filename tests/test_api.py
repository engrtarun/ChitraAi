import asyncio
import httpx

async def test_chat_endpoint():
    print("Testing /api/chat endpoint...")
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                "http://localhost:8000/api/chat",
                json={"message": "Hello, how are you?"},
                timeout=10.0
            )
            print("Status Code:", response.status_code)
            print("Response:", response.json())
        except Exception as e:
            print("Error connecting to API:", e)

if __name__ == "__main__":
    asyncio.run(test_chat_endpoint())
