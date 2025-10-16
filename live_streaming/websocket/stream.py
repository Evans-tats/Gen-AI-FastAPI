from fastapi.websockets import WebSocket

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
        data = await WebSocket.receive_text()
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
        