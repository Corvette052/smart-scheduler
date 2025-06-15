# Smart Scheduler

Set the `ADMIN_EMAILS` environment variable to a comma-separated list if you want booking confirmations sent to multiple addresses. If unset, notifications are sent to `corvette052@gmail.com` by default.

Use `CALENDAR_IDS` to specify one or more Google Calendar IDs (comma-separated) that should receive each booking. If not provided, the single `CALENDAR_ID` variable or a default calendar of `your-account@gmail.com` is used.

Each appointment blocks out two and a half hours which accounts for both the 1.5‑hour tinting job and an additional hour of travel time. For example, a booking at **10:00 AM** will make **12:30 PM** the next available slot.
