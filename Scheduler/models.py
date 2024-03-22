from django.db import models
from dateutil.rrule import rrulestr  # Import rrulestr
from Users.models import CustomUser

class Slots(models.Model): 
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=None)
    start_date = models.DateField(default=None)
    end_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    