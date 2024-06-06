from django.shortcuts import render
from rest_framework.viewsets import generics
from .models import Message
from .serializers import MessageSerializer
from Users.serializers import UserSerializer 
from Users.models import CustomUser 

class MessageList(generics.ListAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    pagination_class = None
    ordering = ('-timestamp')
    
    def get_queryset(self):
        sender_id = self.kwargs.get('sender_id')    
        receiver_id = self.kwargs.get('receiver_id')    
        if sender_id and receiver_id:
            queryset1 = Message.objects.filter(sender=sender_id,receiver=receiver_id)
            queryset2 = Message.objects.filter(sender=receiver_id, receiver=sender_id)
            
            queryset = queryset1.union(queryset2)

            return queryset.order_by('timestamp')

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
            if messages:
                chat_receivers = messages.values_list('receiver_id' ,flat=True).distinct()
                queryset = CustomUser.objects.filter(id__in = chat_receivers)
            else:
                messages = Message.objects.filter(receiver = sender)
                print(messages)
                chat_receivers = messages.values_list('sender_id' , flat=True).distinct()
                queryset = CustomUser.objects.filter(id__in = chat_receivers)


        else:
            queryset = None

        return queryset
