from pydantic import BaseModel

class RAGContentRequest(BaseModel):
    prompt: str

class RAGModelResponse(BaseModel):
    pass