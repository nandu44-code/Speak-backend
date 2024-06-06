from django.urls import path,include
from .views import MessageList
urlpatterns= [
    path('chat/<int:sender_id>/<int:reciever_id>/',MessageList, name="message-list")
]