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
model = genai.GenerativeModel("gemini-2.5-flash")

# Generate a response
response = model.generate_content("Tell me a story.", stream=True)

for chunk in response:
    print(chunk.text, end="", flush=True)

print(response.text)
