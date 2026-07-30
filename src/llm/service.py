from src.config.settings import settings
from src.llm.providers.ollama import OllamaProvider


class LLMService:

    def __init__(self):

        if settings.LLM_PROVIDER == "ollama":
            self.provider = OllamaProvider()

        else:
            raise ValueError(
                f"Unsupported LLM provider: {settings.LLM_PROVIDER}"
            )

    def generate(
        self,
        prompt: str,
    ) -> str:

        return self.provider.generate(prompt)