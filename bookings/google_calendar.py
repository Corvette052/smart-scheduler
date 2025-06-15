import os
import json
from datetime import datetime
import pytz
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Scopes your service account needs
SCOPES = ['https://www.googleapis.com/auth/calendar']

# Load credentials from the environment if present. Importing this module should
# not crash the app if the variable isn't set; instead we'll disable calendar
# functionality.
raw_creds = os.getenv('GOOGLE_CREDS')

service = None
if raw_creds:
    service_account_info = json.loads(raw_creds)
    credentials = service_account.Credentials.from_service_account_info(
        service_account_info, scopes=SCOPES
    )
    service = build('calendar', 'v3', credentials=credentials)
else:
    print(
        "GOOGLE_CREDS env variable not set; Google Calendar integration disabled."
    )

# Which calendar to write to? You can also set this in ENV: CALENDAR_ID
CALENDAR_ID = os.getenv('CALENDAR_ID', 'your-account@gmail.com')


def create_event(summary: str, start_datetime: datetime, end_datetime: datetime):
    """
    Creates an event on your Google Calendar.
    summary: text title
    start_datetime, end_datetime: timezone-naive datetimes in local tz
    """
    # pick your timezone
    tz = os.getenv('CALENDAR_TZ', 'America/New_York')

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

    if service is None:
        print("Google Calendar service not configured; skipping event creation.")
        return None

    try:
        created = service.events().insert(calendarId=CALENDAR_ID, body=event).execute()
        print(f"✅ Event created: {created.get('htmlLink')}")
        return created
    except Exception as e:
        print(f"❌ Failed to create event: {e}")
        return None
