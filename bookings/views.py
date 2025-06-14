from django.shortcuts import render, redirect
from .forms import PublicBookingForm
from .models import Booking
from datetime import datetime, timedelta
from django.core.mail import send_mail
from .google_calendar import create_event

def public_booking_view(request):
    if request.method == 'POST':
        form = PublicBookingForm(request.POST)
        if form.is_valid():
            slot_iso = form.cleaned_data['slot']
            slot_dt = datetime.fromisoformat(slot_iso)

            booking = Booking.objects.create(
                customer=None,  # You can handle this later with user auth
                service_type='Standard Service',
                date=slot_dt.date(),
                start_time=slot_dt.time(),
                end_time=(slot_dt + timedelta(hours=1, minutes=30)).time(),
                address=form.cleaned_data['address'],
                zip_code=form.cleaned_data['zip_code'],
                phone=form.cleaned_data['phone'],
                notes=form.cleaned_data['notes'],
                price=0.00,
                vehicle_type='',
                status='pending',
                email=form.cleaned_data['email'],
                full_name=form.cleaned_data['full_name'],
            )

            # ✅ Create Google Calendar event
            create_event(
                summary=f"{form.cleaned_data['full_name']} - {booking.service_type}",
                start_datetime=datetime.combine(booking.date, booking.start_time),
                end_datetime=datetime.combine(booking.date, booking.end_time)
            )

            # ✅ Send confirmation email
            subject = "Your Appointment is Confirmed"
            message = (
                f"Hi {form.cleaned_data['full_name']},\n\n"
                f"Thank you for booking with us!\n\n"
                f"📅 Date: {booking.date.strftime('%A, %B %d, %Y')}\n"
                f"🕒 Time: {booking.start_time.strftime('%I:%M %p')}\n"
                f"📍 Address: {booking.address}, {booking.zip_code}\n\n"
                f"See you soon!\n"
                f"- Your Company"
            )
            send_mail(subject, message, None, [form.cleaned_data['email']])

            return redirect('/thank-you/')
    else:
        form = PublicBookingForm()

    return render(request, 'bookings/public_booking.html', {'form': form})


def thank_you_view(request):
    return render(request, 'bookings/thank_you.html')
