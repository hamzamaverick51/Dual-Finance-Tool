import os
import google.generativeai as genai

# Make sure your GEMINI_API_KEY is set in your environment or .env
from dotenv import load_dotenv
load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# List all available models for your key
for model in genai.list_models():
    print(model.name) 