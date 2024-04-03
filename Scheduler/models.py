from django.db import models
from dateutil.rrule import rrulestr  # Import rrulestr
from Users.models import CustomUser

class Slots(models.Model): 
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=None, related_name='tutor_slots')
    start_date = models.DateField(default=None)
    end_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    
class Booking(models.Model):
    slot = models.OneToOneField(Slots, on_delete=models.CASCADE, primary_key=True)
    booked_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    booking_time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'),('confirmed', 'Confirmed'), ('cancelled', 'Cancelled')], default='pending')
    amount = models.IntegerField()
    currency = models.CharField(max_length=10)