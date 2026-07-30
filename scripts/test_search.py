from src.database.database import SessionLocal
from src.embeddings.service import EmbeddingService
from src.vector_db.store import VectorStore


#This file is for testing the search functionality we have implemented to get top results from vector database


def main():

    embedding_service = EmbeddingService()
    vector_store = VectorStore()

    while True:

        query = input("\nEnter search query (or 'exit'): ")

        if query.lower() == "exit":
            break

        query_embedding = embedding_service.embed(query)

        results = vector_store.search(
            embedding=query_embedding,
            limit=5,
        )

        print(f"\nFound {len(results)} results\n")

        for i, result in enumerate(results, start=1):

            print("=" * 80)
            print(f"Result #{i}")
            print(f"Score: {result['score']:.4f}")

            payload = result["payload"]

            print(f"Subject : {payload['subject']}")
            print(f"Sender  : {payload['sender']}")
            print(f"Folder  : {payload['folder_name']}")
            print(f"Received: {payload['received_at']}")

            print("\nChunk:")
            print(payload["text"])

            print()


if __name__ == "__main__":
    main()