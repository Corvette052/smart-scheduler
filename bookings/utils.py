from datetime import datetime, timedelta, time
from .models import Booking

WORK_START = time(7, 0)  # <-- Start time changed to 7:00 AM
WORK_END = time(18, 0)
JOB_DURATION = timedelta(hours=1, minutes=30)
TRAVEL_BUFFER = timedelta(hours=1)
BLOCK_TIME = JOB_DURATION + TRAVEL_BUFFER

def get_available_slots():
    slots = []
    now = datetime.now()

    for day in range(7):
        date = now.date() + timedelta(days=day)
        current = datetime.combine(date, WORK_START)
        end = datetime.combine(date, WORK_END)

        while current + JOB_DURATION <= end:
            overlap = Booking.objects.filter(
                date=date,
                start_time__lt=(current + BLOCK_TIME).time(),
                end_time__gt=current.time()
            ).exists()

            if not overlap and current > now:
                slots.append({
                    "label": current.strftime("%A %b %d — %I:%M %p"),
                    "datetime": current
                })

            current += timedelta(minutes=30)  # Move in 30-min intervals

    return slots
