import os
import json
from datetime import datetime
import pytz
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Scopes your service account needs
SCOPES = ['https://www.googleapis.com/auth/calendar']

# Load the raw JSON string from the env var
raw_creds = os.getenv('GOOGLE_CREDS')

service = None
if raw_creds:
    # Parse it
    service_account_info = json.loads(raw_creds)

    # Build credentials object
    credentials = service_account.Credentials.from_service_account_info(
        service_account_info, scopes=SCOPES
    )

    # Construct the Calendar API client
    service = build('calendar', 'v3', credentials=credentials)

# Which calendar to write to? You can also set this in ENV: CALENDAR_ID
CALENDAR_ID = os.getenv('CALENDAR_ID', 'your-account@gmail.com')


def create_event(summary: str, start_datetime: datetime, end_datetime: datetime):
    """
    Creates an event on your Google Calendar.
    summary: text title
    start_datetime, end_datetime: timezone-aware datetimes
    """
    # pick your timezone
    tz = os.getenv('CALENDAR_TZ', 'America/New_York')

    if service is None:
        print("\u274c Google Calendar service not configured. Skipping event creation.")
        return None

    event = {
        'summary': summary,
        'start': {
            'dateTime': start_datetime.astimezone(pytz.timezone(tz)).isoformat(),
            'timeZone': tz,
        },
        'end': {
            'dateTime': end_datetime.astimezone(pytz.timezone(tz)).isoformat(),
            'timeZone': tz,
        },
    }

    try:
        created = service.events().insert(calendarId=CALENDAR_ID, body=event).execute()
        print(f"✅ Event created: {created.get('htmlLink')}")
        return created
    except Exception as e:
        print(f"❌ Failed to create event: {e}")
        return None
