import json
from typing import List


class QueryEnhancement:

    @staticmethod
    def enhance(query: str) -> str:
        prompt = f"""
You are an expert retrieval query optimizer for a Retrieval-Augmented Generation (RAG) system.

Your ONLY task is to generate multiple search queries that will maximize retrieval quality from a vector database.

DO NOT answer the user's question.

Generate 3 different search queries that capture the user's intent from different semantic perspectives.

Guidelines:
1. Preserve the complete information need.
2. Remove conversational language, greetings, and filler.
3. Remove answer-formatting instructions such as:
   - answer in bullet points
   - explain simply
   - keep it short
   - summarize
   - provide examples
4. Keep all important:
   - entities
   - names
   - technical terms
   - dates
   - numbers
   - relationships
5. Each rewritten query should use a different wording while preserving the meaning.
6. Do NOT invent information.
7. Return ONLY valid JSON.
8. Do NOT include markdown.
9. Do NOT include explanations.

Return exactly this format:

{{
    "queries": [
        "query 1",
        "query 2",
        "query 3"
    ]
}}

User Query:
{query}
"""
        return prompt.strip()

    @staticmethod
    def parse_response(response: str) -> List[str]:
        """
        Parse the LLM JSON response into a list of search queries.
        """
        try:
            data = json.loads(response)
            return data.get("queries", [])
        except Exception:
            return []