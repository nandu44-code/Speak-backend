from django.shortcuts import render
from django.http import request
from rest_framework import generics,status
from rest_framework.response import Response
from .models import Slots
from .serializers import SlotSerializer,SlotFilterSerializer
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
        user = self.request.query_params.get('user')
        selected_date = self.request.query_params.get('selected_date')
        if selected_date:
            return Slots.objects.filter(user=user, start_date=selected_date)
        else:
            return Slots.objects.none()