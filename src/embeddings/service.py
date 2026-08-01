from src.config.settings import settings
from src.embeddings.provider_registry import (
    EMBEDDING_PROVIDERS,
)

class EmbeddingService:

    def __init__(self):

        provider = EMBEDDING_PROVIDERS.get(
            settings.EMBEDDING_PROVIDER             #this is stored in .env
        )

        if provider is None:

            raise ValueError(
                f"Unsupported embedding provider: "
                f"{settings.EMBEDDING_PROVIDER}"
            )

        self.provider = provider()

    def generate(
        self,
        text: str,
    ) -> list[float]:

        return self.provider.embed(text)