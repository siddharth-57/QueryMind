from anthropic import Anthropic

from src.config.settings import settings
from src.llm.providers.base import BaseLLMProvider


class AnthropicProvider(BaseLLMProvider):

    def __init__(self):

        self.client = Anthropic(
            api_key=settings.ANTHROPIC_API_KEY,
        )

    def generate(
        self,
        prompt: str,
    ) -> str:

        response = self.client.messages.create(
            model=settings.LLM_MODEL,
            max_tokens=2048,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        )

        return response.content[0].text