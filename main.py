from fastapi import FastAPI
import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load API key from .env
load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

app = FastAPI()

@app.get("/")
def root_controller():
    return {"status" : "healthy"}

@app.get("/chat")
def chat_controller(prompt :str = "inspire me"):
    response = model.generate_content(prompt)
    return{"statement" : response.text}