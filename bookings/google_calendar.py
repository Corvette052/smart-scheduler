import os
import json
from datetime import datetime
import pytz
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Scopes your service account needs
SCOPES = ['https://www.googleapis.com/auth/calendar']

# Load the raw JSON string from the env var.  If not provided we simply disable
# calendar integration instead of crashing the entire application.
raw_creds = os.getenv("GOOGLE_CREDS")

service = None
if raw_creds:
    # Parse it
    service_account_info = json.loads(raw_creds)

    # Build credentials object
    credentials = service_account.Credentials.from_service_account_info(
        service_account_info, scopes=SCOPES
    )

    # Construct the Calendar API client
    service = build("calendar", "v3", credentials=credentials)
else:
    print("⚠️  GOOGLE_CREDS not set; Google Calendar integration disabled.")

# Which calendars to write to. If CALENDAR_IDS is provided, parse it as a
# comma-separated list. Otherwise fall back to a single CALENDAR_ID variable (or
# a default ID).
_cals_env = os.getenv('CALENDAR_IDS')
if _cals_env:
    CALENDAR_IDS = [cid.strip() for cid in _cals_env.split(',') if cid.strip()]
else:
    CALENDAR_IDS = [os.getenv('CALENDAR_ID', 'your-account@gmail.com')]


def create_event(summary: str, start_datetime: datetime, end_datetime: datetime):
    """
    Creates an event on your Google Calendar.
    summary: text title
    start_datetime, end_datetime: timezone-naive datetimes in local tz
    """
    # pick your timezone
    tz = os.getenv('CALENDAR_TZ', 'America/New_York')

    if service is None:
        print("⚠️  Google Calendar service not configured; skipping event creation.")
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

    created_event = None
    for cal_id in CALENDAR_IDS:
        try:
            created_event = service.events().insert(calendarId=cal_id, body=event).execute()
            print(f"✅ Event created on {cal_id}: {created_event.get('htmlLink')}")
        except Exception as e:
            print(f"❌ Failed to create event on {cal_id}: {e}")

    return created_event
