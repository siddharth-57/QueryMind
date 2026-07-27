from abc import ABC, abstractmethod

# Every provider should support the same operations: authenticate & fetch emails
# Whether it's Gmail, Outlook, or another provider doesn't matter they will have to enforce these methods.
# This gives us a contract that every provider must follow.

class EmailProvider(ABC):
    """
    Base interface for all email providers.
    """

    @abstractmethod
    def authenticate(self) -> None:
        """
        Authenticate with the email provider.
        """
        pass

    @abstractmethod
    def fetch_emails(self):
        """
        Fetch emails from the provider.
        """
        pass