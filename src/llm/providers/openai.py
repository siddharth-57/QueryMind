from openai import OpenAI

from src.config.settings import settings
from src.llm.providers.base import BaseLLMProvider


class OpenAIProvider(BaseLLMProvider):

    def __init__(self):

        self.client = OpenAI(
            api_key=settings.OPENAI_API_KEY,
        )

    def generate(
        self,
        prompt: str,
    ) -> str:

        response = self.client.chat.completions.create(
            model=settings.LLM_MODEL,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        )

        return response.choices[0].message.content