from fastapi import Body
from loguru import logger

from .utils_service import vector_service
from .schema import RAGContentRequest
from .transform import embed

async def get_rag_content(body : RAGContentRequest = Body(...)):
    logger.info(f"Received RAG prompt: {body.prompt}")
    rag_content = await vector_service.search(
        "knowledge_base", embed(body.prompt), top_k=5, score_threshold=0.2
    )
    logger.info(f"Raw RAG content result: {rag_content}")
    rag_content_str = "\n".join(
        [c.payload["text"] for c in rag_content]
    )
    logger.info(f"Extracted RAG content string:\n{rag_content_str}")
    return rag_content_str