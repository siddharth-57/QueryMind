#This file checks unchunked emails, gets them chunks them and then stores them in the database
# using the relevant methods

from src.preprocessing.cleaning import EmailCleaningService
from src.preprocessing.chunking import EmailChunkingService

from src.repositories.email_repository import EmailRepository
from src.repositories.chunk_repository import ChunkRepository


class EmailPreprocessingPipeline:

    def __init__(self, db):
        self.email_repository = EmailRepository(db)
        self.chunk_repository = ChunkRepository(db)

        self.cleaner = EmailCleaningService()
        self.chunker = EmailChunkingService()

    def process(self) -> int:

        processed = 0

        emails = self.email_repository.get_unchunked_emails()

        for email in emails:

            cleaned_body = self.cleaner.clean(email.body)

            chunks = self.chunker.chunk_email(cleaned_body)

            self.chunk_repository.create_chunks(
                email.id,
                chunks,
            )

            self.email_repository.mark_as_chunked(email.id)

            processed += 1

        return processed