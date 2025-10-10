from sentence_transformers import SentenceTransformer
import re
import aiofiles

embedder = SentenceTransformer("jinaai/jina-embeddings-v2-base-en")

DEFAULT_CHUNK_SIZE = 1024 * 1024 * 50
async def load(file_path: str, chunk_size: int):
    async with aiofiles.open(file_path, "r", encoding="utf-8") as f:
        while chunk := await f.read(chunk_size):
            yield chunk

def clean(text: str) -> str:
    t = text.replace("\n", " ")
    t = re.sub(r"\s+", " ", t)
    t = re.sub(r"\. ,", "", t)
    t = t.replace("..", ".")
    t = t.replace(". .", ".")
    cleaned_text = t.replace("\n", " ").strip()
    return cleaned_text

def embed(text: str):
    return embedder.encode(text).tolist()