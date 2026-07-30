from sqlalchemy.orm import Session

from src.database.models import EmailChunk
from sqlalchemy.orm import joinedload


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
    
    
# This method fetches all chunks from email_chunks table to be converted into embeddings and stored in vector db
# Without joinedload, SQLAlchemy may execute one query to fetch all chunks and then an additional query for each related email as you access chunk.email
# With joinedload, it performs a single query that fetches the chunks and their associated emails together. For an indexing job that processes every chunk, this is much more efficient.
# later incremental indexing will be added 
    def get_all_chunks(self) -> list[EmailChunk]:
        return (
            self.db.query(EmailChunk)
            .options(joinedload(EmailChunk.email))
            .order_by(EmailChunk.created_at)
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
        
    