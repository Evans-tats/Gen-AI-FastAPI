import asyncio
from google import generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

class GeminiChatStream:
    def __init__(self):
        self.model = genai.GenerativeModel("gemini-2.5-flash")
    

    async def chat_stream(self, prompt: str):
        def sync_stream():
            return self.model.generate_content(prompt, stream=True)
        response = await asyncio.to_thread(sync_stream)
        for chunk in response:
            if chunk.text:
                yield f"data: {chunk.text}\n\n"
            await asyncio.sleep(0.05)
        yield f"data : [DONE]\n\n"        