from Scheduler.models import Booking
from rest_framework  import serializers
class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['slot','booked_by']
