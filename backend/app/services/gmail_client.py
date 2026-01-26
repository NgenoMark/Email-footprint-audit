from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build


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

    def list_messages(self, query: str, max_results: int = 50) -> list[dict]:
        response = (
            self._service.users()
            .messages()
            .list(userId="me", q=query, maxResults=max_results)
            .execute()
        )
        return response.get("messages", [])

    def get_message(self, message_id: str) -> dict:
        return (
            self._service.users()
            .messages()
            .get(
                userId="me",
                id=message_id,
                format="metadata",
                metadataHeaders=["From", "Subject", "Date"],
            )
            .execute()
        )
