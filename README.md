# Smart Scheduler

This Django project integrates with Google Calendar. To authorize API access, provide your service account credentials in the `GOOGLE_CREDS` environment variable.

Set `GOOGLE_CREDS` to the **entire JSON string** from your Google service account key. The application will parse this variable at runtime.

Optionally, define `CALENDAR_ID` to target a specific calendar and `CALENDAR_TZ` for your desired timezone.
