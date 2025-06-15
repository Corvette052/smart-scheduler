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

        bookings = list(Booking.objects.filter(date=date))

        while current + JOB_DURATION <= end:
            overlap = False

            for booking in bookings:
                booking_start = datetime.combine(date, booking.start_time)
                block_end = booking_start + BLOCK_TIME

                if booking_start <= current < block_end:
                    overlap = True
                    break

            if not overlap and current > now:
                slots.append({
                    "label": current.strftime("%A %b %d — %I:%M %p"),
                    "datetime": current
                })

            current += timedelta(minutes=30)  # Move in 30-min intervals

    return slots
