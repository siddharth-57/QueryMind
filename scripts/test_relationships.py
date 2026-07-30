from src.database.database import SessionLocal
from src.repositories.chunk_repository import ChunkRepository


def main():
    db = SessionLocal()

    try:
        repo = ChunkRepository(db)

        chunks = repo.get_all_chunks()

        print(f"Found {len(chunks)} chunks\n")

        if not chunks:
            print("No chunks found.")
            return

        chunk = chunks[0]

        print("Chunk Information")
        print("-" * 40)
        print(f"Chunk ID      : {chunk.id}")
        print(f"Email ID      : {chunk.email_id}")
        print(f"Chunk Index   : {chunk.chunk_index}")
        print(f"Content       : {chunk.content[:100]}")

        print()

        print("Parent Email")
        print("-" * 40)
        print(f"Subject       : {chunk.email.subject}")
        print(f"Sender        : {chunk.email.sender}")
        print(f"Folder        : {chunk.email.folder_name}")
        print(f"Received At   : {chunk.email.received_at}")

    finally:
        db.close()


if __name__ == "__main__":
    main()