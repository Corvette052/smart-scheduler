# bookings/views.py

from django.shortcuts import render, redirect
from django.conf import settings
from django.core.mail import send_mail
import os

from .forms import PublicBookingForm
from .models import Booking
from .google_calendar import create_event

from datetime import datetime, timedelta
import pytz

# Use the same timezone as Google Calendar so times match exactly
tz_name = os.getenv("CALENDAR_TZ", "America/New_York")
local_tz = pytz.timezone(tz_name)

# Additional email address to receive booking notifications
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "corvette052@gmail.com")

def public_booking_view(request):
    if request.method == 'POST':
        form = PublicBookingForm(request.POST)
        if form.is_valid():
            # —————————————————————————————————————————
            # 1) parse the ISO string; if it's naive, localize it;
            #    otherwise, convert it into the local timezone properly
            slot_iso = form.cleaned_data['slot']              # e.g. "2025-06-15T08:00:00-04:00"
            slot_dt  = datetime.fromisoformat(slot_iso)

            if slot_dt.tzinfo is None:
                # no offset ⇒ assume local timezone
                slot_dt = local_tz.localize(slot_dt)
            else:
                # already has an offset ⇒ convert into local timezone
                slot_dt = slot_dt.astimezone(local_tz)

            # 2) compute end time
            end_dt = slot_dt + timedelta(hours=1, minutes=30)
            # —————————————————————————————————————————

            # 3) save booking (SQLite can't handle tz-aware TimeFields)
            booking = Booking.objects.create(
                customer     = None,
                service_type = 'Standard Service',
                date         = slot_dt.date(),
                # SQLite cannot store timezone-aware times, so strip tzinfo
                start_time   = slot_dt.time(),
                end_time     = end_dt.time(),
                address      = form.cleaned_data['address'],
                zip_code     = form.cleaned_data['zip_code'],
                phone        = form.cleaned_data['phone'],
                notes        = form.cleaned_data['notes'],
                price        = 0.00,
                vehicle_type = '',
                status       = 'pending',
                email        = form.cleaned_data['email'],
                full_name    = form.cleaned_data['full_name'],
            )

            # 4) push to Google Calendar
            create_event(
                summary        = f"{booking.full_name} – {booking.service_type}",
                start_datetime = slot_dt,
                end_datetime   = end_dt
            )

            # 5) send confirmation email
            subject = "Your Appointment is Confirmed"
            message = (
                f"Hi {booking.full_name},\n\n"
                "Thanks for booking!\n\n"
                f"📅 {booking.date:%A, %B %d, %Y}\n"
                f"🕒 {booking.start_time:%I:%M %p}\n"
                f"📍 {booking.address}, {booking.zip_code}\n\n"
                "See you soon!\n— Your Company"
            )
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [booking.email, ADMIN_EMAIL]
            )

            return redirect('thank_you')
    else:
        form = PublicBookingForm()

    return render(request, 'bookings/public_booking.html', {'form': form})


def thank_you_view(request):
    """Simple page displayed after a successful booking."""
    return render(request, 'bookings/thank_you.html')

