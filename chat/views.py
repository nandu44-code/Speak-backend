from django.shortcuts import render
from rest_framework.viewsets import generics
from .models import Message
from .serializers import MessageSerializer
# Create your views here.

class MessageList(generics.ListAPIView):
    queryset = Message.objects.all()
    serizlizer_class = MessageSerializer
    ordering = ('-timestamp')
    
    def get_queryset(self):
        sender_id = self.kwargs.get('sender_id')    
        reciever_id = self.kwargs.get('reciever_id')    
        if sender_id and reciever_id:
            queryset = Message.objects.filter(sender=sender_id,reciever=reciever_id)
        else:
            queryset = None
        return queryset
