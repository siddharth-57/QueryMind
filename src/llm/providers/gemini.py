from google import genai

from src.config.settings import settings
from src.llm.providers.base import BaseLLMProvider


class GeminiProvider(BaseLLMProvider):

    def __init__(self):

        self.client = genai.Client(
            api_key=settings.GOOGLE_API_KEY,
        )

    def generate(
        self,
        prompt: str,
    ) -> str:

        response = self.client.models.generate_content(
            model=settings.LLM_MODEL,
            contents=prompt,
        )

        return response.text