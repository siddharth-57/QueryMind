# The Retrieval Service is the orchestrator.
# responsibility is: question->embedding->vector search->context->llm->answer
# it doesn't implement any AI logic itself.
# it coordinates four independent components that we've already built.

from src.embeddings.service import EmbeddingService
from src.llm.service import LLMService
from src.retrieval.prompt_builder import PromptBuilder
from src.retrieval.query_enhancement import QueryEnhancement
from src.vector_db.store import VectorStore


class RetrievalService:

    def __init__(self):

        self.embedding_service = EmbeddingService()

        self.vector_store = VectorStore()

        self.llm_service = LLMService()
        
        self.enhancement_service = QueryEnhancement()

# This method gives the final answer of the user query after passing the entire rag pipeline 
    def answer(
        self,
        query: str,
    ) -> str:
    
        enhancement_prompt = self.enhancement_service.enhance(query)
    
        llm_response = self.llm_service.generate(
            enhancement_prompt
        )
    
        search_queries = (
            self.enhancement_service.parse_response(
                llm_response
            )
        )
    
        all_results = []
    
        for search_query in search_queries:
        
            embedding = self.embedding_service.embed(
                search_query
            )
    
            results = self.vector_store.search(
                embedding=embedding
            )
    
            all_results.extend(results)
    
        unique_contexts = []
        seen = set()
    
        for result in all_results:
        
            text = result["payload"]["text"]
    
            if text not in seen:
                seen.add(text)
                unique_contexts.append(text)
    
        prompt = PromptBuilder.build(
            query=query,
            contexts=unique_contexts,
        )
    
        final_answer = self.llm_service.generate(
            prompt
        )
    
        return final_answer