from django.shortcuts import render
from django.http import request
from rest_framework import generics,status,viewsets
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Slots,Booking
from .serializers import SlotSerializer,SlotFilterSerializer,BookingSerializer,BookingSerializerStudent
from dateutil.rrule import rrulestr
import datetime
# Create your views here.

class SlotListCreateView(generics.ListCreateAPIView):
    queryset = Slots.objects.all()
    serializer_class = SlotSerializer
    
    def create(self, request, *args, **kwargs):
        print('coign herereee...')
        serializer = self.get_serializer(data=request.data)
        print('coign herereee...')
        print(request.data)
        serializer.is_valid(raise_exception=True)
        print('coign herereee...')
        slots = serializer.save() 
        headers = self.get_success_headers(slots)
        return Response(SlotSerializer(slots, many=True).data, status=status.HTTP_201_CREATED, headers=headers)

class SlotDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Slots.objects.all()
    serializer_class = SlotSerializer

class SlotFilterView(generics.ListAPIView):
    serializer_class = SlotFilterSerializer


    def get_queryset(self):
        user = self.request.query_params.get('created_by')
        print(user)
        selected_date = self.request.query_params.get('selected_date')
        print(selected_date)
        print('hooyyyyyyyyyyyyym,hjjjjjjjjjjjjjjjjjjjjjjjhhkh')
        slotss = Slots.objects.filter(created_by=user, start_date=selected_date)
        for i in slotss:
            print(i)
        if selected_date:
            return Slots.objects.filter(created_by=user, start_date=selected_date)
        else:
            return Slots.objects.none()

class BookingView(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    
@api_view(['GET'])
def GetBookings(request, tutor, status):
    print('get_bookings',tutor,status)
    try:
        print('entering in to the try block')
        bookings = Booking.objects.filter(slot__created_by_id=tutor, status=status)
        print('number of bookings',bookings.count())
        serializer = BookingSerializer(bookings, many=True)
        
        return Response(serializer.data)
    except Exception as e:
        return Response({'error': str(e)}, status=400)

@api_view(['GET'])
def GetBookingsStudent(request, user,status):
    print("entering here")
    try:
        bookings = Booking.objects.filter(booked_by=user, status=status)
        print('number of bookings',bookings.count())
        serializer = BookingSerializerStudent(bookings, many=True)

        return Response(serializer.data)
    except:
        return Response({"error":str(e)}, status=400)

class BookingDeleteView(APIView):
    def delete(self, request, slot, format=None):
        print("coming here,,")
        try:
            print(slot)
            booking = Booking.objects.get(pk=slot)
            booking.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Booking.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
