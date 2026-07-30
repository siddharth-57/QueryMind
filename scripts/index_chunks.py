from src.database.database import SessionLocal

from src.repositories.chunk_repository import ChunkRepository

from src.embeddings.service import EmbeddingService

from src.vector_db.store import VectorStore


def main():

    db = SessionLocal()
    success_count=0
    failure_count=0

    try:

        repository = ChunkRepository(db)

        embedding_service = EmbeddingService()

        vector_store = VectorStore()

        chunks = repository.get_all_chunks()

        print(f"Found {len(chunks)} chunks.\n")

        for chunk in chunks:
            try:
                embedding = embedding_service.embed(
                    chunk.content
                )

                payload = {
                    "email_id": str(chunk.email_id),
                    "chunk_index": chunk.chunk_index,
                    "text": chunk.content,
                    "subject": chunk.email.subject,
                    "sender": chunk.email.sender,
                    "received_at": chunk.email.received_at.isoformat(),
                    "folder_name": chunk.email.folder_name,
                }

                vector_store.upsert(
                    point_id=chunk.id,
                    embedding=embedding,
                    payload=payload,
                )

                print(
                    f"✓ Indexed chunk "
                    f"{chunk.chunk_index} "
                    f"({chunk.email.subject})"
                )
                success_count+=1
                
            except Exception as e:
                failure_count+=1
                print(f"Failed to index chunk {chunk.id}: {e}")
            
        print("\nIndexing completed successfully.")
        print(vector_store.count())
        print(f"Failed chunk insertions: {failure_count}")
            
    finally:
        db.close()
        
if __name__ == "__main__":
    main()