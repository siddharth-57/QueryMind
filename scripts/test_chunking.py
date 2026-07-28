from src.preprocessing.chunking import EmailChunkingService

service = EmailChunkingService(chunk_size=20)

text = (
    "This is a simple email that will be split "
    "into multiple chunks."
)

print(service.chunk_email(text))
