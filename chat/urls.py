from django.urls import path,include
from .views import MessageList, ChatRecieversList
urlpatterns= [
    path('chat/<int:sender_id>/<int:reciever_id>/',MessageList.as_view(), name="message-list"),
    path('chat/recievers/<int:sender_id>/', ChatRecieversList.as_view(), name='chat-receivers-list')
]