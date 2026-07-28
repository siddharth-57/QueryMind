from src.preprocessing.chunking import EmailChunkingService


service = EmailChunkingService(chunk_size=100)


email = """
Project Alpha

Authentication module has been completed successfully.

Payment module is currently under testing.

Deployment is planned for Friday.

Below is a very long paragraph.

{}
""".format(
    "Lorem ipsum " * 100
)

chunks = service.chunk_email(email)

print("=" * 70)

for index, chunk in enumerate(chunks, start=1):
    print(f"\nChunk {index}")
    print("-" * 70)
    print(chunk)
    print()
    print(f"Characters: {len(chunk)}")