import os
from loguru import logger

from .transform import load, clean, embed
from .utils import VectorRepository

class vectortService(VectorRepository):
    def __init__(self):
        super().__init__()
    
    async def store_file_content_in_db(
            self, file_path :str, chunk_size :int =512, collection_name :str ="kowledge_base", collection_vector_size :int =768
    ):
        await self.create_collection(collection_name, collection_vector_size)
        logger.info(f"Storing content of file {file_path} in the database")
        async for chunk in load(file_path, chunk_size):
            logger.debug(f"inserting '{chunk[0:20]}......' into the database")
            embedding_vectors = embed(clean(chunk))
            file_name = os.path.basename(file_path)
            await self.create(
                collection_name, embedding_vectors, chunk, file_name
            )

vector_service = vectortService()