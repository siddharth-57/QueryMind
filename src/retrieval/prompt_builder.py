from typing import List


class PromptBuilder:

    @staticmethod
    def build(
        query: str,
        contexts: List[str],
    ) -> str:

        context = "\n\n".join(contexts)

        prompt = f"""
You are a helpful AI assistant.

Answer the user's question using ONLY the information provided in the context below.

If the answer cannot be found in the context, say that you don't know.

Context:
{context}

Question:
{query}

Answer:
"""

        return prompt.strip()