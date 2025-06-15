from django.contrib import admin
from django.urls import path
from django.shortcuts import redirect
from bookings import views

urlpatterns = [
    path('', lambda request: redirect('booking', permanent=False)),  # Redirect /
    path('admin/', admin.site.urls),
    path('book/', views.public_booking_view, name='booking'),
    path('claim-offer/', views.marketing_form_view, name='claim_offer'),
    path('thank-you/', views.thank_you_view, name='thank_you'),
]
