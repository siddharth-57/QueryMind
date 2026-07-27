from src.ingestion.providers.base import EmailProvider
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from src.ingestion.providers.base import EmailProvider


# Google OAuth works using scopes, which define what permissions your application requests.
# We're only reading emails, so gmail.readonly follows the principle of least privilege.

SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
]

class GmailProvider(EmailProvider):

    def __init__(self):
        self.service = None

    def authenticate(self):
        creds = None
    
        token_path = Path("token.json")
        credentials_path = Path("credentials.json")
    
        if token_path.exists():
            creds = Credentials.from_authorized_user_file(
                token_path,
                SCOPES,
            )
    
        if not creds or not creds.valid:
        
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
    
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    credentials_path,
                    SCOPES,
                )
    
                creds = flow.run_local_server(port=0)
    
            token_path.write_text(
                creds.to_json(),
                encoding="utf-8",
            )
    
        self.service = build(       # Creates the Gmail client. Every Gmail API call will use:
            "gmail",
            "v1",
            credentials=creds,
        )
    
    def fetch_emails(self):
        """
        Will fetch emails from Gmail.
        """
        pass