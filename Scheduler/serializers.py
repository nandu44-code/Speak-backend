from rest_framework import serializers
from .models import Slots,Booking
from Users.models import CustomUser
from datetime import timedelta , datetime

class SlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slots
        fields = ['id','created_by', 'start_date', 'end_date', 'start_time', 'end_time']

    def validate(self, attrs):
        start_date = attrs.get('start_date')
        end_date = attrs.get('end_date')

        # Validate maximum of 5 days
        if (end_date - start_date).days > 5:
            raise serializers.ValidationError("Maximum 5 days are allowed.")

        # Validate start time is before end time
        if attrs['start_time'] >= attrs['end_time']:
            raise serializers.ValidationError("Start time must be before end time.")

        return attrs

    def create(self, validated_data):
        user_id = validated_data.pop('created_by')
        print(user_id)
        user = CustomUser.objects.get(email=user_id)         
        print(user)
        slots = []
        current_date = validated_data['start_date']
        while current_date <= validated_data['end_date']:
            current_datetime = datetime.combine(current_date, validated_data['start_time'])
            while current_datetime.time() < validated_data['end_time']:
                slot = Slots(
                    created_by = user,
                    start_time=current_datetime.time(),
                    end_time=(current_datetime + timedelta(hours=1)).time(),
                    start_date=current_datetime.date(),
                    end_date=current_datetime.date() + timedelta(days=1) if current_datetime.time() >= validated_data['end_time'] else current_date,  # Handle end_date logic for last slot
                )
                slots.append(slot)
                current_datetime += timedelta(hours=1)
            current_date += timedelta(days=1)

        return Slots.objects.bulk_create(slots)

class SlotFilterSerializer(serializers.ModelSerializer):
    print('slot filter serializer')
    class Meta:
        model = Slots
        fields = '__all__'

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'

class BookingSerializerStudent(serializers.ModelSerializer):
    slots_data = serializers.SerializerMethodField()

    class Meta:
        model = Booking
        fields = ['slot', 'booked_by', 'booking_time', 'status', 'amount', 'currency', 'slots_data']

    def get_slots_data(self, obj):
        slots = SlotSerializer(obj.slot).data
        return slots

class BookingSerializerAdmin(serializers.ModelSerializer):

    slot_details = SlotSerializer(source='slot', read_only=True)  # Include slot details in booking serializer
    class Meta:
        model = Booking
        fields = ['slot', 'booked_by', 'booking_time', 'status', 'amount', 'currency', 'slot_details']