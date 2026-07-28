from textwrap import wrap
# Python already provides a robust implementation that:
# prefers breaking at whitespace, avoids splitting words in half and is deterministic

class EmailChunkingService:
    """
    Splits cleaned email text into semantically meaningful chunks.

    The algorithm tries to preserve paragraph boundaries.
    Very large paragraphs are split using textwrap as a fallback.
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

        if not body.strip():
            return []

        paragraphs = [
            paragraph.strip()
            for paragraph in body.split("\n\n")
            if paragraph.strip()
        ]

        chunks = []
        current_chunk = ""

        for paragraph in paragraphs:

            # Paragraph itself is too large.
            if len(paragraph) > self.chunk_size:

                if current_chunk:
                    chunks.append(current_chunk.strip())
                    current_chunk = ""

                large_chunks = wrap(
                    paragraph,
                    width=self.chunk_size,
                    break_long_words=False,
                    replace_whitespace=False,
                    drop_whitespace=False,
                )

                chunks.extend(
                    chunk.strip()
                    for chunk in large_chunks
                    if chunk.strip()
                )

                continue

            proposed_chunk = (
                paragraph
                if not current_chunk
                else current_chunk + "\n\n" + paragraph
            )

            if len(proposed_chunk) <= self.chunk_size:
                current_chunk = proposed_chunk
            else:
                chunks.append(current_chunk.strip())
                current_chunk = paragraph

        if current_chunk:
            chunks.append(current_chunk.strip())

        return chunks