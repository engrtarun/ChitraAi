# ChitraAi - Chat Backend Architecture (Corrected)

## DeepSeek's Red Flags Fixed

1. **Puter.js Architecture Fix**:
   - `edge-chat` folder has been completely **deleted**.
   - Puter.js is a client-side library and should be executed natively inside the user's browser via the `video-generator-ui` frontend (e.g. LobeChat/TypeScript UI).
   - Attempting to wrap Puter.js in a Node server is insecure, violates ToS (requires raw credentials), and is an anti-pattern.

2. **Backend Fallback Role**:
   - The Python FastAPI backend now acts purely as a **Fallback API**.
   - If the browser Puter.js request fails or is rate-limited, the frontend will call `http://localhost:8000/api/chat`.
   - The backend will then route the request to **Groq** (Primary Fallback) or **Gemini** (Secondary Fallback).

3. **Missing Tests Added**:
   - Added `test_groq.py` and `test_gemini.py` to the `/tests` folder.
   - You can run these independently once you set up the `.env`.

4. **Environment & Setup Ready**:
   - Python `venv` has been set up.
   - All `requirements.txt` dependencies have been installed (FastAPI, Groq, Google Generative AI).

## Setup Status
✅ **Python FastAPI Backend (`/backend`)**:
- Clean `main.py` ready to handle Fallback.
- `config.py` cleaned of Puter plain-text credentials.

✅ **Tests (`/tests`)**:
- Setup `test_api.py`, `test_groq.py`, and `test_gemini.py`.

## Next Steps
1. Add your real API keys to the `.env` file for Groq and Gemini.
2. Activate your environment: `.\.venv\Scripts\Activate.ps1`
3. Run tests to verify the keys: 
   - `python tests/test_groq.py`
   - `python tests/test_gemini.py`
4. Run the Python Fallback Server: 
   - `cd backend && uvicorn main:app --reload`
5. Have your UI friend implement Puter.js in the browser, with an Axios/Fetch catch block that points to this backend if Puter fails.
