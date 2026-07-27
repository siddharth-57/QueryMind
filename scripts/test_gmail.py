# Before downloading emails, checks if authentication to Gmail works.

from src.ingestion.providers.gmail import GmailProvider


def main():
    provider = GmailProvider()

    provider.authenticate()

    print("Successfully authenticated with Gmail!")


if __name__ == "__main__":
    main()