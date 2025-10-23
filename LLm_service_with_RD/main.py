from fastapi import FastAPI
from contextlib import asynccontextmanager
from routers.conversation import router as conversation_router

from database_connection import init_db,engine

@asynccontextmanager
async def lifespan(_: FastAPI):
    await init_db()
    yield
    await engine.dispose()

app = FastAPI(lifespan=lifespan)

app.include_router(conversation_router)
