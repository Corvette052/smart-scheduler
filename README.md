# Smart Scheduler

Set the `ADMIN_EMAILS` environment variable to a comma-separated list to send
booking confirmations to additional addresses. If unset, notifications are
also sent to `corvette052@gmail.com` by default.

Use `CALENDAR_IDS` to specify one or more Google Calendar IDs (comma-separated)
that should receive each booking. If not provided, the single `CALENDAR_ID`
variable or a default calendar of `your-account@gmail.com` is used.
