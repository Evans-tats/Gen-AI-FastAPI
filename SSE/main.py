from fastapi import FastAPI , Body
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from typing import Annotated 

from stream import GeminiChatStream

app = FastAPI()

app.mount("/pages", StaticFiles(directory="pages"), name="pages")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/generate/text/stream")
async def serve_text_to_text_stream_controller(
    prompt : str
) -> StreamingResponse:
    return StreamingResponse(
        GeminiChatStream().chat_stream(prompt),media_type="text/event-stream"
    )

@app.post("/generate/text/stream")
async def serve_text_to_text_stream_controller(
    body : Annotated[dict, Body(...)]
) -> StreamingResponse:
    prompt = body.get("prompt","")
    return StreamingResponse(
        GeminiChatStream().chat_stream(prompt),media_type="text/event-stream"
    )