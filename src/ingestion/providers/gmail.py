from src.ingestion.providers.base import EmailProvider
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from src.ingestion.providers.base import EmailProvider
import base64

from datetime import datetime
from email.utils import parsedate_to_datetime

from src.models.email_message import EmailMessage
from bs4 import BeautifulSoup
from googleapiclient.errors import HttpError

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
    
# Gmail first returns message ids of the emails and then for each message id we can fetch the entire email associated with it
    def fetch_emails(self, max_results: int = 10) -> list[EmailMessage]:
        results = (
            self.service.users()
            .messages()
            .list(
                userId="me",
                maxResults=max_results,
            )
            .execute()
        )
    
        parsed_emails = []

        for message in results.get("messages", []):
            parsed_emails.append(
                self._fetch_and_parse_email(
                    message["id"]
                )
            )

        return parsed_emails
    
# This method helps us get the full emails associated with message ids     
    def get_email(self, message_id: str):
        return (
            self.service.users()
            .messages()
            .get(
                userId="me",
                id=message_id,
                format="full",
            )
            .execute()
        )
    
# The Gmail API stores headers as a list, Searching that list repeatedly is inefficient, hence we convert it into a dictionary.
    def _extract_headers(self, payload: dict) -> dict:
        headers = {}

        for header in payload.get("headers", []):
            headers[header["name"]] = header["value"]

        return headers
    
# Walking the MIME Tree
    def _walk_parts(self, part: dict):
        yield part

        for child in part.get("parts", []):
            yield from self._walk_parts(child)
            


    def _clean_html(self, html: str) -> str:
        soup = BeautifulSoup(html, "html.parser")

        return soup.get_text(
            separator="\n",
            strip=True,
        )
            
            
# Extract the Email Body
    def _extract_body(self, payload: dict) -> str:
        html_body = None

        for part in self._walk_parts(payload):

            mime_type = part.get("mimeType")

            body = part.get("body", {})

            data = body.get("data")

            if not data:
                continue

            decoded = base64.urlsafe_b64decode(data).decode(
                "utf-8",
                errors="replace",
            )

            if mime_type == "text/plain":
                return decoded

            if mime_type == "text/html":
                html_body = self._clean_html(decoded)

        return html_body or ""
    
    
# Detect Attachments
    def _has_attachments(self, payload: dict) -> bool:
        for part in self._walk_parts(payload):

            if part.get("filename"):
                return True

        return False
    
# A single parser that returns the internal EmailMessage object
    def _parse_email(self, message: dict) -> EmailMessage:
        payload = message["payload"]
    
        headers = self._extract_headers(payload)
    
        # Parse received time
        try:
            received_at = parsedate_to_datetime(headers["Date"])
        except Exception:
            received_at = datetime.fromtimestamp(
                int(message["internalDate"]) / 1000
            )
    
        body = self._extract_body(payload)
    
        has_attachments = self._has_attachments(payload)
    
        # -------- New Fields --------
    
        conversation_id = message["threadId"]
    
        internet_message_id = headers.get("Message-ID")
    
        labels = message.get("labelIds", [])
        folder_name = labels[0] if labels else "UNKNOWN"
    
        # ----------------------------
    
        return EmailMessage(
            message_id=message["id"],
            conversation_id=conversation_id,
            internet_message_id=internet_message_id,
            folder_name=folder_name,
    
            subject=headers.get("Subject", ""),
            sender=headers.get("From", ""),
            recipients=headers.get("To", ""),
    
            body=body,
            received_at=received_at,
            has_attachments=has_attachments,
        )
        
#Gmail exposes the mailbox's current history ID through profile API. each email is associated with a history ID
# history ID exposes the mailbox's current state
# this method will help save the latest history ID after a successfull sync
# we first store the emails and then get the latest history id and store it in syncstate table
# next fetching of emails start after the latest point of history in the syncstate table 
    def get_latest_history_id(self) -> str:
        """
        Returns the latest history ID of the Gmail mailbox.
        """

        profile = (
            self.service.users()
            .getProfile(userId="me")
            .execute()
        )

        return profile["historyId"]
    
    
# This function gets the changes since the last history Id.
# Note: Gmail's history API doesn't return emails, it returns message Ids since the last history Id. we must download these emails using these message Ids
    def get_history(self, start_history_id: str) -> list:
        response = (
            self.service.users()
            .history()
            .list(
                userId="me",
                startHistoryId=start_history_id,
            )
            .execute()
        )

        return response.get("history", [])
    
    
    
# Extract the message Ids of the latest Emails 
    def extract_message_ids(self, history: list) -> list[str]:
        message_ids = set()         #Gmail can sometimes report the same message multiple times in history hence we need to use set here

        for record in history:
            for item in record.get("messagesAdded", []):
                message = item.get("message")

                if not message:
                    continue

                if "DRAFT" in message.get("labelIds", []):      #ignores draft messages
                    continue

                message_ids.add(message["id"])

        return list(message_ids)
    
    
    
# Helper function to be used in methods for fetching email 
    def _fetch_and_parse_email(self, message_id: str,) -> EmailMessage:
        return self._parse_email(
            self.get_email(message_id)
            )
    
    
# for the message Ids of the latest emails given by gmail we fetch the full emails and parse them and return them
    def fetch_emails_by_ids(self, message_ids: list[str], ) -> list[EmailMessage]:
        parsed_emails = []

        for message_id in message_ids:
            try:
                parsed_emails.append(
                    self._fetch_and_parse_email(message_id)
                )
            # error handling for deleted messages as their history id still exists
            except HttpError as e:
                if e.resp.status == 404:
                    print(
                        f"Skipping message '{message_id}' because it no longer exists."
                    )
                    continue

                raise

        return parsed_emails