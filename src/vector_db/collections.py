# Responsibilities:
# Check whether the collection already exists.
# If it exists, do nothing.
# Otherwise create it with: vector size = 2560 and cosine distance

from qdrant_client.models import Distance
from qdrant_client.models import VectorParams

from src.config.settings import settings
from src.vector_db.client import get_qdrant_client


def create_collection_if_not_exists() -> None:
    """
    Creates the Qdrant collection if it doesn't already exist.
    """

    client = get_qdrant_client()

    collections = client.get_collections()

    existing = [
        collection.name
        for collection in collections.collections
    ]

    if settings.QDRANT_COLLECTION in existing:
        print(
            f"Collection '{settings.QDRANT_COLLECTION}' already exists."
        )
        return

    client.create_collection(
        collection_name=settings.QDRANT_COLLECTION,
        vectors_config=VectorParams(
            size=settings.EMBEDDING_DIMENSION,
            distance=Distance.COSINE,
        ),
    )

    print(
        f"Collection '{settings.QDRANT_COLLECTION}' created successfully."
    )