from loguru import logger
from qdrant_client import AsyncQdrantClient
from qdrant_client.http import models
from qdrant_client.http.models import ScoredPoint

class VectorRepository:
    def __init__(self, host: str = "localhost", port:int =6333):
        self.db_client = AsyncQdrantClient(host=host, port=port)
    
    async def create_collection(self, collection_name: str, vector_size: int):
        vectors_config = models.VectorParams(size=vector_size, distance=models.Distance.COSINE)
        
        response = await self.db_client.get_collections()
        collection_exists = any(collection_name == collection.name for collection in response.collections)
        if collection_exists:
            logger.info(f"Collection {collection_name} already exists")
            logger.info("recreating it")
            await self.db_client.delete_collection(collection_name=collection_name)
            return await self.db_client.create_collection(collection_name=collection_name, vectors_config=vectors_config)       
        logger.info(f"Creating collection {collection_name}")
        return await self.db_client.create_collection(collection_name=collection_name, 
                                                      vectors_config=vectors_config)
    
    async def delete_collection(self, collection_name: str):
        return await self.db_client.delete_collection(collection_name=collection_name)
    
    async def create(self, collection_name :str,embedding_vector: list[float], original_text: str, source: str) -> None:
        response = await self.db_client.count(collection_name=collection_name)
        logger.info(
            f"creating a new vector with id {response.count}"
            f"inside collection {collection_name}"
        )
        await self.db_client.upsert(
            collection_name=collection_name,
            points=[
                models.PointStruct(
                    id=response.count,
                    vector=embedding_vector,
                    payload={
                        "text": original_text,
                        "source": source
                    }
                )
            ]
        )
    async def search(
            self , collection_name:str, query_vector: list[float], top_k: int, score_threshold: float
    ):
        logger.debug(
            f"searching for relevant items in th {collection_name} collection"
        )
        response = await self.db_client.query_points(
            collection_name=collection_name,
            query=query_vector,
            limit=top_k,
            score_threshold=score_threshold,
            with_payload=True
        )
        if response.points:
            logger.info(f"Found {len(response.points)} results. Top score: {response.points[0].score:.4f}")
        else:
            logger.info("No results found for query.")
        return response.points
    