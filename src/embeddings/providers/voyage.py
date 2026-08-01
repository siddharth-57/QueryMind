import voyageai

from src.config.settings import settings
from src.embeddings.providers.base import EmbeddingProvider


class VoyageProvider(EmbeddingProvider):

    def __init__(self):

        self.client = voyageai.Client(
            api_key=settings.VOYAGE_API_KEY,
        )

    def embed(
        self,
        text: str,
    ) -> list[float]:

        response = self.client.embed(
            [text],
            model=settings.EMBEDDING_MODEL,
        )

        return response.embeddings[0]