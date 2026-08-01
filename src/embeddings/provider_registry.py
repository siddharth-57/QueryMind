from src.embeddings.providers.ollama import OllamaEmbeddingProvider
from src.embeddings.providers.openai import OpenAIProvider
from src.embeddings.providers.voyage import VoyageProvider


#Storing the classes not the objects

EMBEDDING_PROVIDERS = {
    "ollama": OllamaEmbeddingProvider,
    "openai": OpenAIProvider,
    "voyage": VoyageProvider,
}


#provider = EMBEDDING_PROVIDERS["ollama"]() this can later be used to create objects