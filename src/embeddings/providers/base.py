from abc import ABC, abstractmethod


class EmbeddingProvider(ABC):
# Every embedding provider must guarantee the embed function.
    @abstractmethod
    def embed(self, text: str) -> list[float]:
        """
        Generates an embedding for the supplied text.
        """
        pass