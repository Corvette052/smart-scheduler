from google.oauth2 import service_account
from googleapiclient.discovery import build
from datetime import datetime, timedelta
import pytz

# Path to your service account credentials JSON file
SERVICE_ACCOUNT_FILE = 'bookings/credentials.json'

# Define the scopes
SCOPES = ['https://www.googleapis.com/auth/calendar']

# Load credentials
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
)

# Build the service
service = build('calendar', 'v3', credentials=credentials)

# 👇 Replace this with YOUR Gmail address (the calendar you want to use)
calendar_id = 'wilterq@gmail.com'


def create_event(summary, start_datetime, end_datetime):
    """Creates an event on your Google Calendar."""
    timezone = 'America/New_York'
    event = {
        'summary': summary,
        'start': {
            'dateTime': start_datetime.isoformat(),
            'timeZone': timezone,
        },
        'end': {
            'dateTime': end_datetime.isoformat(),
            'timeZone': timezone,
        },
    }

    try:
        created_event = service.events().insert(calendarId=calendar_id, body=event).execute()
        print(f"✅ Event created: {created_event.get('htmlLink')}")
        return created_event
    except Exception as e:
        print(f"❌ Failed to create event: {e}")
        return None
