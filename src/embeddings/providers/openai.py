from openai import OpenAI

from src.config.settings import settings
from src.embeddings.providers.base import BaseEmbeddingProvider


class OpenAIProvider(BaseEmbeddingProvider):

    def __init__(self):

        self.client = OpenAI(
            api_key=settings.OPENAI_API_KEY,
        )

    def embed(
        self,
        text: str,
    ) -> list[float]:

        response = self.client.embeddings.create(
            model=settings.EMBEDDING_MODEL,
            input=text,
        )

        return response.data[0].embedding