import os
from datetime import timedelta
from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from models import User

SCOPES = ["https://www.googleapis.com/auth/calendar.events"]

client_config = {
    "web": {
        "client_id": os.getenv("GOOGLE_CLIENT_ID"),
        "client_secret": os.getenv("GOOGLE_CLIENT_SECRET"),
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "redirect_uris": [os.getenv("GOOGLE_REDIRECT_URI")],
    }
}
# http://localhost:8000/docs
class CalendarService:

    def _get_credentials(self, user: User) -> Credentials:
        if not user.calendar_connected:
            raise ValueError("User has not connected their Google Calendar")

        creds = Credentials(
            token=None,
            refresh_token=user.google_refresh_token,
            token_uri="https://oauth2.googleapis.com/token",
            client_id=os.getenv("GOOGLE_CLIENT_ID"),
            client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
            scopes=SCOPES,
        )
        creds.refresh(Request())
        return creds
    
    def get_authorization_url(self, state: str) -> str:
        flow = Flow.from_client_config(
            client_config,
            scopes=SCOPES,
            redirect_uri=os.getenv("GOOGLE_REDIRECT_URI")
        )
        authorization_url, _ = flow.authorization_url(
            state=state,
            access_type="offline",
            prompt="consent"
        )
        return authorization_url
    
    def exchange_code_for_tokens(self, code: str) -> dict:
        flow = Flow.from_client_config(
            client_config,
            scopes=SCOPES,
            redirect_uri=os.getenv("GOOGLE_REDIRECT_URI")
        )
        flow.fetch_token(code=code)
        return {
            "access_token": flow.credentials.token,
            "refresh_token": flow.credentials.refresh_token,
        }

    def create_event(self, user: User, summary: str, description: str, start_date_time: str, end_date_time: str):
        creds = self._get_credentials(user)
        service = build("calendar", "v3", credentials=creds)

        event = {
            'summary': summary,
            'description': description,
            'start': {
                'dateTime': start_date_time,
                'timeZone': 'America/Sao_Paulo',
            },
            'end': {
                'dateTime': end_date_time,
                'timeZone': 'America/Sao_Paulo',
            },
        }

        event = service.events().insert(calendarId='primary', body=event).execute()
        return event
