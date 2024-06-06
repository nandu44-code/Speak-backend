from django.shortcuts import render
from rest_framework.viewsets import generics
from .models import Message
from .serializers import MessageSerializer
from Users.serializers import UserSerializer 
from Users.models import CustomUser 

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

class ChatRecieversList(generics.ListAPIView):
    serializer_class = UserSerializer
    ordering = ('-timestamp')
    
    def get_queryset(self):
        sender = self.kwargs.get('sender_id')
        if sender:
            messages = Message.objects.filter(sender = sender)
            chat_receivers = messages.values_list('receiver_id' ,flat=True).distinct()
            queryset = CustomUser.objects.filter(id__in = chat_receivers)
        else:
            queryset = None

        return queryset
