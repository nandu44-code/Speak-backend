# chat/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model
from .models import Message

User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.username = self.scope['url_route']['kwargs']['username']
        self.room_group_name = f'chat_{self.username}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        receiver_username = text_data_json['receiver']

        # Retrieve the sender and receiver from the database
        try:
            sender = self.scope['user']
            receiver = User.objects.get(username=receiver_username)

            # Save the message to the database
            message_instance = Message.objects.create(
                sender=sender,
                receiver=receiver,
                content=message
            )

            # Send the message to the receiver's group
            await self.channel_layer.group_send(
                f'chat_{receiver_username}',
                {
                    'type': 'chat_message',
                    'message': message,
                    'sender': sender.username
                }
            )
        except User.DoesNotExist:
            # Handle the case where the receiver does not exist
            await self.send(text_data=json.dumps({
                'error': 'User does not exist.'
            }))

    async def chat_message(self, event):
        message = event['message']
        sender = event['sender']

        await self.send(text_data=json.dumps({
            'message': message,
            'sender': sender
        }))
