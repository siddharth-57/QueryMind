from uuid import UUID

from qdrant_client.models import PointStruct

from src.vector_db.client import get_qdrant_client
from src.config.settings import settings

#This file simply has the implementation for storing in vector database
class VectorStore:
    def __init__(self):
        self.client = get_qdrant_client()


    def upsert(
        self,
        point_id: UUID,
        embedding: list[float],
        payload: dict,
    ) -> None:
        """
        Store or update a single vector in Qdrant.
        """

        point = PointStruct(
            id=str(point_id),
            vector=embedding,
            payload=payload,
        )

        self.client.upsert(
            collection_name=settings.QDRANT_COLLECTION,
            points=[point],
        )
    
    
    def count(self) -> int:
        """
        Return the number of vectors stored in the collection.
        """

        response = self.client.count(
            collection_name=settings.QDRANT_COLLECTION,
            exact=True,
        )

        return response.count