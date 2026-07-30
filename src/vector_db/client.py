# This file has one responsibility only: Return a configured Qdrant client.
# It should not: create collections, insert vectors, perform searches
# It only manages the connection.

from qdrant_client import QdrantClient

from src.config.settings import settings


def get_qdrant_client() -> QdrantClient:
    """
    Returns a configured Qdrant client.
    """

    return QdrantClient(
        url=settings.QDRANT_URL
    )