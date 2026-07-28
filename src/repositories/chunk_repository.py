from sqlalchemy.orm import Session

from src.database.models import EmailChunk


class ChunkRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_chunks(
        self,
        email_id,
        chunks: list[str],
    ) -> list[EmailChunk]:
        """
        Store all chunks belonging to a single email.
        """

        db_chunks = []

        for index, chunk in enumerate(chunks):
            db_chunk = EmailChunk(
                email_id=email_id,
                chunk_index=index,
                content=chunk,
            )

            self.db.add(db_chunk)
            db_chunks.append(db_chunk)

        self.db.commit()

        for chunk in db_chunks:
            self.db.refresh(chunk)

        return db_chunks

    def get_chunks_by_email_id(
        self,
        email_id,
    ) -> list[EmailChunk]:
        """
        Fetch every stored chunk for an email.
        """

        return (
            self.db.query(EmailChunk)
            .filter(
                EmailChunk.email_id == email_id
            )
            .order_by(
                EmailChunk.chunk_index
            )
            .all()
        )

    def delete_chunks(
        self,
        email_id,
    ) -> None:
        """
        Remove every chunk belonging to an email.
        """

        (
            self.db.query(EmailChunk)
            .filter(
                EmailChunk.email_id == email_id
            )
            .delete()
        )

        self.db.commit()