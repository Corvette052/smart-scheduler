# Smart Scheduler

Set the `ADMIN_EMAILS` environment variable to a comma-separated list if you want booking confirmations sent to multiple addresses. If unset, notifications are sent to `corvette052@gmail.com` by default.

Use `CALENDAR_IDS` to specify one or more Google Calendar IDs (comma-separated) that should receive each booking. If not provided, the single `CALENDAR_ID` variable or a default calendar of `your-account@gmail.com` is used.

Each appointment blocks out two and a half hours which accounts for both the 1.5‑hour tinting job and an additional hour of travel time. For example, a booking at **10:00 AM** will make **12:30 PM** the next available slot.

## Required environment variables

The following variables must be provided through your environment or secret
manager:

- `SECRET_KEY` – Django secret key.
- `EMAIL_HOST_USER` – email account used to send booking confirmations.
- `EMAIL_HOST_PASSWORD` – app password for the above account.
- `GOOGLE_CREDS` – JSON credentials for the Google Calendar service account.
- `GHL_API_KEY` – API key used to create contacts in GoHighLevel.
- `GHL_LOCATION_ID` – location ID for your GoHighLevel account. If omitted, the application attempts to decode it from the JWT-formatted `GHL_API_KEY`.

To enable GoHighLevel integration, set `GHL_API_KEY` in your environment. The token
looks like a JWT string (three segments separated by dots). The location ID
is extracted automatically, so a typical `.env` snippet might look like:

```env
GHL_API_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```
You can explicitly set `GHL_LOCATION_ID` if you prefer to override the decoded value.

If `EMAIL_HOST_USER` and `EMAIL_HOST_PASSWORD` are omitted, the application now
logs a warning and continues without sending emails. Bookings are still saved
and added to Google Calendar.

## Initial setup

After deploying to a new environment, run migrations to create the SQLite database:

```bash
python manage.py migrate
```

This step is required the first time the app runs on Railway since the container starts with an empty filesystem.
