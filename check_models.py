"""Check available Gemini models"""
import os
from google import genai

# Set API key
os.environ["GOOGLE_API_KEY"] = "AIzaSyAsNyR53Ldlmff-zCeHvdsVKcilxo6e2xE"

client = genai.Client()

print("Available models:")
print("-" * 50)

try:
    models = client.models.list()
    for model in models:
        print(f"- {model.name}")
        if hasattr(model, 'supported_generation_methods'):
            print(f"  Methods: {model.supported_generation_methods}")
except Exception as e:
    print(f"Error: {e}")
