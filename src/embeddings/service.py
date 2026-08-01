from src.config.settings import settings

from src.embeddings.providers.ollama import OllamaEmbeddingProvider
from src.embeddings.providers.openai import OpenAIProvider
from src.embeddings.providers.voyage import VoyageProvider


class EmbeddingService:

    def __init__(self):

        if settings.EMBEDDING_PROVIDER == "ollama":
            self.provider = OllamaEmbeddingProvider()
            
        elif settings.EMBEDDING_PROVIDER == "openai":
            self.provider = OpenAIProvider()
        
        elif settings.EMBEDDING_PROVIDER == "voyage":
            self.provider = VoyageProvider()
        
        else:
            raise ValueError(
                f"Unsupported embedding provider: "
                f"{settings.EMBEDDING_PROVIDER}"
            )

    def embed(self, text: str) -> list[float]:
        return self.provider.embed(text)