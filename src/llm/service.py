from src.config.settings import settings
from src.llm.provider_registry import (
    LLM_PROVIDERS,
)


class LLMService:

    def __init__(self):

        provider = LLM_PROVIDERS.get(
            settings.LLM_PROVIDER
        )

        if provider is None:

            raise ValueError(
                f"Unsupported LLM provider: "
                f"{settings.LLM_PROVIDER}"
            )

        self.provider = provider()

    def generate(
        self,
        prompt: str,
    ) -> str:

        return self.provider.generate(prompt)