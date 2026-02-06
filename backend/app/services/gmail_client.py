import time

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


class GmailClient:
    def __init__(
        self,
        access_token: str,
        refresh_token: str,
        client_id: str,
        client_secret: str,
        token_uri: str,
        scopes: list[str],
    ) -> None:
        self._creds = Credentials(
            token=access_token,
            refresh_token=refresh_token,
            token_uri=token_uri,
            client_id=client_id,
            client_secret=client_secret,
            scopes=scopes,
        )
        if self._creds.expired and self._creds.refresh_token:
            self._creds.refresh(Request())
        self._service = build("gmail", "v1", credentials=self._creds, cache_discovery=False)

    def get_profile_email(self) -> str:
        profile = self._service.users().getProfile(userId="me").execute()
        return profile.get("emailAddress", "")

    def list_messages(
        self,
        query: str,
        max_results: int = 50,
        page_token: str | None = None,
    ) -> dict:
        request = self._service.users().messages().list(
            userId="me", q=query, maxResults=max_results, pageToken=page_token
        )
        return self._execute_with_backoff(request.execute)

    def get_message(self, message_id: str) -> dict:
        request = (
            self._service.users()
            .messages()
            .get(
                userId="me",
                id=message_id,
                format="metadata",
                metadataHeaders=["From", "Subject", "Date"],
            )
        )
        return self._execute_with_backoff(request.execute)

    def _execute_with_backoff(self, func, retries: int = 5, base: float = 0.5):
        for attempt in range(retries):
            try:
                return func()
            except HttpError as exc:
                if attempt == retries - 1:
                    raise
                sleep_for = base * (2 ** attempt)
                time.sleep(sleep_for)
            except OSError:
                if attempt == retries - 1:
                    raise
                time.sleep(base * (2 ** attempt))
