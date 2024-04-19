from django.shortcuts import render
from django.http import request
from rest_framework import generics,status,viewsets,pagination
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Slots,Booking
from .serializers import SlotSerializer,SlotFilterSerializer,BookingSerializer,BookingSerializerStudent,BookingSerializerAdmin
from dateutil.rrule import rrulestr
import datetime
from django.db.models import Prefetch

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
    
# @api_view(['GET'])
# def GetBookings(request, tutor, status):
#     print('get_bookings',tutor,status)
#     try:
#         print('entering in to the try block')
#         bookings = Booking.objects.filter(slot__created_by_id=tutor, status=status)
#         print('number of bookings',bookings.count())
#         serializer = BookingSerializer(bookings, many=True)
        
#         return Response(serializer.data)
#     except Exception as e:
#         return Response({'error': str(e)}, status=400)

# @api_view(['GET'])
# def GetBookings(request, tutor, status):
#     print('get_bookings', tutor, status)
#     try:
#         print('entering in to the try block')
#         bookings = Slots.objects.filter(
#             created_by_id=tutor, 
#             booking__status= status, 
#             booking__isnull=False
#         ).select_related('booking')
        
#         if not bookings.exists():
#             print('no bookings found here')
#             return Response({'message': 'No bookings found'}, status=404)

#         print('number of bookings', bookings.count())
#         try:
#             serialized_data = BookingSerializerAdmin(bookings, many=True).data
#             print(serialized_data)
#             return Response(serialized_data)
#         except Exception as e:
#             print(f"Error in serialization: {e}")
#             traceback.print_exc()  # Print the traceback
#             return Response({'error': 'Error in serialization'}, status=400)
        
#         return Response(serializer.data)
#     except Exception as e:
#         return Response({'error': str(e)}, status=400)

class SlotsBookingViewSet(viewsets.ViewSet):
    def list(self, request):
        try:
            tutor = request.query_params.get('tutor')
            status = request.query_params.get('status')
            
            print('tutor',tutor, 'status', status)
            slots = Slots.objects.filter(created_by=tutor)
            bookings = Booking.objects.filter(slot__in=slots)

            if status:
                bookings = bookings.filter(status=status)
            print(bookings)
            serializer = BookingSerializerAdmin(bookings, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({'error': str(e)}, status=400)

@api_view(['GET'])
def GetBookingsStudent(request, user,status):
    print("entering here")
    try:
        bookings = Booking.objects.filter(booked_by_id=user, status=status)
        print('number of bookings',bookings.count())
        serializer = BookingSerializerStudent(bookings, many=True)

        return Response(serializer.data)
    except:
        return Response({"error"}, status=400)
@api_view(['GET'])
def GetBookingsStudent(request, user,status):
    print("entering here")
    try:
        bookings = Booking.objects.filter(booked_by_id=user, status=status)
        print('number of bookings',bookings.count())
        serializer = BookingSerializerAdmin(bookings, many=True)

        return Response(serializer.data)
    except:
        return Response({"error"}, status=400)

class BookingDeleteView(APIView):
    def delete(self, request, slot, format=None):
        print("coming here,,")
        try:
            print(slot)
            slots=Slots.objects.get(id=slot)
            if slots:
                slots.is_booked=False
                slots.save()
            booking = Booking.objects.get(slot=slot)
            print(booking)
            booking.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Booking.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def get_all_bookings(request):
    # paginator = paginationPageNumberPagination()
    try:
        bookings = Booking.objects.all()
        print(bookings.count,'bookings-count')
        serializer = BookingSerializerAdmin(bookings, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response({'error': str(e)}, status=400)
