"""Check available Gemini models.

This script lists available Gemini models using the GOOGLE_API_KEY
from your environment. It is for local debugging only and should
never contain hard-coded secrets.
"""
import os
from google import genai

# Expect GOOGLE_API_KEY to be set in the environment (or via .env loaded elsewhere)
if not os.getenv("GOOGLE_API_KEY"):
    raise RuntimeError(
        "GOOGLE_API_KEY is not set. Set it in your environment before running this script."
    )

client = genai.Client(api_key=os.environ["GOOGLE_API_KEY"])

print("Available models:")
print("-" * 50)

try:
    models = client.models.list()
    for model in models:
        print(f"- {model.name}")
        if hasattr(model, "supported_generation_methods"):
            print(f"  Methods: {model.supported_generation_methods}")
except Exception as e:
    print(f"Error: {e}")
