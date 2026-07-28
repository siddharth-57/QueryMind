from textwrap import wrap
# Python already provides a robust implementation that:
# prefers breaking at whitespace, avoids splitting words in half and is deterministic


class EmailChunkingService:
    """
    Splits an email body into smaller chunks suitable
    for embedding models.
    """

    def __init__(
        self,
        chunk_size: int = 1000,
    ):
        self.chunk_size = chunk_size

    def chunk_email(
        self,
        body: str,
    ) -> list[str]:
        """
        Split an email into fixed-size chunks.

        Empty chunks are discarded.
        """

        if not body.strip():
            return []

        chunks = wrap(
            body,
            width=self.chunk_size,
            break_long_words=False,
            replace_whitespace=False,
            drop_whitespace=False,
        )

        return [
            chunk.strip()
            for chunk in chunks
            if chunk.strip()
        ]