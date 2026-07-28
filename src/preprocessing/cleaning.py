import re


class EmailCleaningService:
    """
    Performs lossless preprocessing on email text.

    These operations normalize formatting without removing
    potentially useful information.
    """

    def clean(
        self,
        text: str,
    ) -> str:
        if not text:
            return ""

        # Normalize Windows line endings.
        text = text.replace("\r\n", "\n")

        # Normalize old Mac line endings.
        text = text.replace("\r", "\n")

        # Remove trailing whitespace.
        text = re.sub(
            r"[ \t]+$",
            "",
            text,
            flags=re.MULTILINE,
        )

        # Collapse 3+ blank lines into 2.
        text = re.sub(
            r"\n{3,}",
            "\n\n",
            text,
        )

        # Remove leading/trailing whitespace.
        text = text.strip()

        return text