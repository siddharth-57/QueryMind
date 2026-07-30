# This file contains ollama implementation for embedding texts

import ollama

from src.config.settings import settings
from src.embeddings.providers.base import EmbeddingProvider


class OllamaEmbeddingProvider(EmbeddingProvider):

    def embed(self, text: str) -> list[float]:

        response = ollama.embed(
            model=settings.EMBEDDING_MODEL,
            input=text,
        )
# because it can embed multiple texts at once. We're embedding one chunk at a time. So we return the first embedding.
        return response["embeddings"][0]    
    