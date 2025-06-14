from django.db import models
from django.contrib.auth.models import User

class Booking(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=255)
    zip_code = models.CharField(max_length=10)
    notes = models.TextField(blank=True)
    service_type = models.CharField(max_length=100)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    vehicle_type = models.CharField(max_length=50, blank=True)
    status = models.CharField(max_length=50, default='pending')

    def __str__(self):
        return f"{self.full_name} - {self.date} at {self.start_time}"
