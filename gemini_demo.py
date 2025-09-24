import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load API key from .env
load_dotenv()

# Optional: Reduce noisy GRPC logs
os.environ["GRPC_VERBOSITY"] = "ERROR"

# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Choose a model
model = genai.GenerativeModel("gemini-1.5-flash")

# Generate a response
response = model.generate_content("Write a haiku about FastAPI and AI.")
print(response.text)
