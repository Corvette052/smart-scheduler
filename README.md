# Smart Scheduler

This Django project requires several environment variables for configuration.
Create a `.env` file based on the provided `.env.example` and set the values for
production.

```
cp .env.example .env
# then edit .env and fill in your secrets
```

The variables include:
- `SECRET_KEY` — Django secret key.
- `EMAIL_HOST_USER` and `EMAIL_HOST_PASSWORD` — credentials for sending email.
- `GOOGLE_CREDS` — Google service account JSON used by the calendar integration.

`bookings/credentials.json` and `Smart Scheduler Sync.json` have been removed
from version control. Store any sensitive JSON credentials in the environment
instead of committing them to the repository.
