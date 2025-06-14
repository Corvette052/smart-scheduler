from django.contrib import admin
from django.urls import path
from bookings import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('book/', views.public_booking_view, name='booking'),
    path('thank-you/', views.thank_you_view, name='thank_you'),
]
