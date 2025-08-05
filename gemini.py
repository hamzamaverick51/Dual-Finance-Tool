# services/gemini.py

import os
from typing import Optional
import google.generativeai as genai

# ✅ Load API Key securely
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise EnvironmentError("❌ GEMINI_API_KEY is not set in environment variables.")

# ✅ Configure Gemini
genai.configure(api_key=api_key)

# Using the most capable and stable available model for text generation
MODEL_NAME = "models/gemini-2.5-flash-lite"


# ✅ Gemini summarization function
def gemini_summary(prompt: str) -> Optional[str]:
    try:
        model = genai.GenerativeModel(MODEL_NAME)
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"[❌ Gemini Error] Failed to generate content: {e}")
        return None
