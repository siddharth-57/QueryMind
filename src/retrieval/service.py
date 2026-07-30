# The Retrieval Service is the orchestrator.
# responsibility is: question->embedding->vector search->context->llm->answer
# it doesn't implement any AI logic itself.
# it coordinates four independent components that we've already built.

from src.embeddings.service import EmbeddingService
from src.llm.service import LLMService
from src.retrieval.prompt_builder import PromptBuilder
from src.vector_db.store import VectorStore


class RetrievalService:

    def __init__(self):

        self.embedding_service = EmbeddingService()

        self.vector_store = VectorStore()

        self.llm_service = LLMService()

# this method gives the final answer of the user query after passing the entire rag pipeline 
    def answer(
        self,
        query: str,
    ) -> str:

        query_embedding = self.embedding_service.embed(query)

        results = self.vector_store.search(
            embedding=query_embedding,
        )

        contexts = [
            result["payload"]["text"]
            for result in results
        ]

        prompt = PromptBuilder.build(
            query=query,
            contexts=contexts,
        )

        answer = self.llm_service.generate(
            prompt
        )

        return answer