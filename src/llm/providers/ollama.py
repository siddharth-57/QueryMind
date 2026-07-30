from ollama import chat

from src.config.settings import settings
from src.llm.providers.base import BaseLLMProvider


class OllamaProvider(BaseLLMProvider):

    def generate(
        self,
        prompt: str,
    ) -> str:

        response = chat(
            model=settings.LLM_MODEL,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        )

        return response.message.content