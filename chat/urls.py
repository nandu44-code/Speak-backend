from django.urls import path,include
from .views import MessageList, ChatRecieversList
urlpatterns= [
    path('chat/messages/<int:sender_id>/<int:receiver_id>/',MessageList.as_view(), name="message-list"),
    path('chat/receivers/<int:sender_id>/', ChatRecieversList.as_view(), name='chat-receivers-list')
]