from src.config.settings import settings

from src.embeddings.providers.ollama import (
    OllamaEmbeddingProvider,
)


class EmbeddingService:

    def __init__(self):

        if settings.EMBEDDING_PROVIDER == "ollama":
            self.provider = OllamaEmbeddingProvider()

        else:
            raise ValueError(
                f"Unsupported embedding provider: "
                f"{settings.EMBEDDING_PROVIDER}"
            )

    def embed(self, text: str) -> list[float]:

        return self.provider.embed(text)