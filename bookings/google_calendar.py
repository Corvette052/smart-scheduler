import os
import json
from datetime import datetime
import pytz
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Scopes your service account needs
SCOPES = ['https://www.googleapis.com/auth/calendar']


# Load the raw JSON string from the env var. When running locally the
# ``GOOGLE_CREDS`` variable may not be provided. Instead of raising an error
# and crashing the app, gracefully disable the calendar integration so the rest
# of the site can still function.
raw_creds = os.getenv("GOOGLE_CREDS")
service = None

if raw_creds:
    try:
        # Parse the JSON credentials and construct the Calendar API client
        service_account_info = json.loads(raw_creds)
        credentials = service_account.Credentials.from_service_account_info(
            service_account_info, scopes=SCOPES
        )
        service = build("calendar", "v3", credentials=credentials)
    except Exception as e:
        # If anything goes wrong (malformed JSON, etc.), log the issue and
        # continue without Google Calendar enabled.
        print(f"Failed to configure Google Calendar service: {e}")
else:
    # Environment variable missing
    print("GOOGLE_CREDS not set. Google Calendar integration disabled.")

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

    if service is None:
        # No Google Calendar credentials configured, so simply skip creating the
        # event. Returning None keeps the calling code simple.
        print("Google Calendar service not configured; skipping event creation.")
        return None

    event = {
        "summary": summary,
        "start": {
            "dateTime": start_datetime.astimezone(pytz.timezone(tz)).isoformat(),
            "timeZone": tz,
        },
        "end": {
            "dateTime": end_datetime.astimezone(pytz.timezone(tz)).isoformat(),
            "timeZone": tz,
        },
    }

    try:
        created = service.events().insert(calendarId=CALENDAR_ID, body=event).execute()
        print(f"✅ Event created: {created.get('htmlLink')}")
        return created
    except Exception as e:
        print(f"❌ Failed to create event: {e}")
        return None
