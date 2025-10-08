from transformers import Automodel
import re
import aiofiles

embedder = Automodel.from_pretrained("jinaai/jina-embediings-v2-base-en", trust_remote_code=True)

DEFAULT_CHUNK_SIZE = 1024 * 1024 * 50
async def load(file_path: str):
    async with aiofiles.open(file_path, "r", encoding="utf-8") as f:
        if chunk := await f.read(DEFAULT_CHUNK_SIZE):
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