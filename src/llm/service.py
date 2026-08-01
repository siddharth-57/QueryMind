from src.config.settings import settings
from src.llm.providers.ollama import OllamaProvider
from src.llm.providers.openai import OpenAIProvider
from src.llm.providers.anthropic import AnthropicProvider
from src.llm.providers.gemini import GeminiProvider

class LLMService:

    def __init__(self):

        if settings.LLM_PROVIDER == "ollama":
            self.provider = OllamaProvider()

        elif settings.LLM_PROVIDER == "openai":
            self.provider = OpenAIProvider()

        elif settings.LLM_PROVIDER == "anthropic":
            self.provider = AnthropicProvider()

        elif settings.LLM_PROVIDER == "gemini":
            self.provider = GeminiProvider()

        else:
            raise ValueError(
                f"Unsupported LLM provider: {settings.LLM_PROVIDER}"
            )

    def generate(
        self,
        prompt: str,
    ) -> str:

        return self.provider.generate(prompt)