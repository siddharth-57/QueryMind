# Before downloading emails, checks if authentication to Gmail works.

from src.ingestion.providers.gmail import GmailProvider


def main():
    provider = GmailProvider()

    provider.authenticate()

    emails = provider.fetch_emails(max_results=3)

    for email in emails:
        print("=" * 80)
        print(f"Subject      : {email.subject}")
        print(f"From         : {email.sender}")
        print(f"To           : {email.recipients}")
        print(f"Received At  : {email.received_at}")
        print(f"Attachments  : {email.has_attachments}")
        print()
        print(email.body[:500])
        print()


if __name__ == "__main__":
    main()