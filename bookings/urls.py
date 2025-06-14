from django.urls import path
from . import views

urlpatterns = [
    path('', views.public_booking_view, name='booking'),
    path('thank-you/', views.thank_you_view, name='thank_you'),
]
