from fastapi.websockets import WebSocket
import asyncio
from typing import AsyncGenerator
from google import generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

class WebSocketConnectionManager:
    def __init__(self):
        self.active_connections : list[WebSocket] = []
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
    async def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
        await websocket.close()
    
    async def broadcast(self, message: str | bytes | dict):
        for connection in self.active_connections:
            await self.send(connection, message)

    @staticmethod
    async def receive(websocket: WebSocket) -> str:
        data = await websocket.receive_text()
        return data
    
    @staticmethod
    async def send(websocket: WebSocket, message: str | bytes | dict):
        if isinstance(message, str):
            await websocket.send_text(message)
        elif isinstance(message, bytes):
            await websocket.send_bytes(message)
        elif isinstance(message, dict):
            await websocket.send_json(message)
        else:
            raise ValueError("Message must be str, bytes, or dict")

ws_manager = WebSocketConnectionManager()

class WebSocketStream:
    def __init__(self):
        self.model = genai.GenerativeModel("gemini-2.5-flash")

    async def chat_stream(
            self, prompt: str, mode: str = "sse"
    ) -> AsyncGenerator[str, None]:
        def sync_stream():
            return self.model.generate_content(prompt, stream=True)
        
        response = await asyncio.to_thread(sync_stream)
        for chunk in response:
            yield (
                f"data: {chunk.text}\n\n"
                if mode == "sse"
                else chunk.text
            )
            await asyncio.sleep(0.05)
        if mode == "sse":
            yield f"data: [DONE]\n\n"
        