from pydantic import BaseModel
from typing import Literal

class ModelRequest(BaseModel):
    prompt :str

class TextModelRequest(ModelRequest):
    model : Literal["gemini-1.5-flash"]