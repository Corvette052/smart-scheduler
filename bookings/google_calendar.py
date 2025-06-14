import os
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build
from datetime import datetime, timedelta

# Get the one-line JSON string from environment
GOOGLE_CREDS_STRING = os.getenv("GOOGLE_CREDS")

if not GOOGLE_CREDS_STRING:
    raise ValueError("GOOGLE_CREDS env variable not set.")

creds_dict = json.loads(GOOGLE_CREDS_STRING)
credentials = service_account.Credentials.from_service_account_info(creds_dict)

service = build("calendar", "v3", credentials=credentials)

calendar_id = "wilterq@gmail.com"  # Replace if needed

def create_event(summary, start_datetime, end_datetime):
    timezone = "America/New_York"
    event = {
        "summary": summary,
        "start": {
            "dateTime": start_datetime.isoformat(),
            "timeZone": timezone,
        },
        "end": {
            "dateTime": end_datetime.isoformat(),
            "timeZone": timezone,
        },
    }

    try:
        created_event = service.events().insert(calendarId=calendar_id, body=event).execute()
        print(f"✅ Event created: {created_event.get('htmlLink')}")
        return created_event
    except Exception as e:
        print(f"❌ Failed to create event: {e}")
        return None

