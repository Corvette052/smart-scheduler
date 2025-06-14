from django.contrib import admin
from django.urls import path
from bookings.views import public_booking_view, thank_you_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('book/', public_booking_view, name='public_booking'),
    path('thank-you/', thank_you_view, name='thank_you'),
]
