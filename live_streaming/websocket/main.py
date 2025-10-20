from fastapi import FastAPI,WebSocket
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.websockets import WebSocket, WebSocketDisconnect
from loguru import logger

from stream import ws_manager, WebSocketStream


app = FastAPI()
app.mount("/pages", StaticFiles(directory="pages"), name="pages")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.websocket("/ws/chat")
async def websocket_chat_endpoint(websocket: WebSocket):
    logger.info("WebSocket connection requested")
    await ws_manager.connect(websocket)
    stream_handler = WebSocketStream()
    try:
        while True:
            prompt = await ws_manager.receive(websocket)
            logger.info(f"Received prompt: {prompt}")
            async for chunk in stream_handler.chat_stream(prompt, mode="wb"):
                await ws_manager.send(websocket, chunk)
    except WebSocketDisconnect:
        logger.info("WebSocket disconnected")
    except Exception as e:
        logger.error(f"Error: {e}")
    finally:
        await ws_manager.disconnect(websocket)