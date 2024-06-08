# chat/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from .models import Message
from Users.models import CustomUser
User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.sender_id = self.scope['url_route']['kwargs']['sender_id']
        self.receiver_id = self.scope['url_route']['kwargs']['receiver_id'] 
        if self.sender_id and self.receiver_id and self.sender_id > self.receiver_id:
            self.room_group_name = f'chat_{self.receiver_id}_{self.sender_id}'
        else:
            self.room_group_name = f'chat_{self.sender_id}_{self.receiver_id}'

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

        # Retrieve the sender and receiver from the database
        try:
            sender = await self.get_sender()
            receiver = await self.get_receiver()

            # Save the message to the database
            message_instance = await self.create_message_instance(sender, receiver, message)

            # Send the message to the receiver's group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'sender': sender.id
                }
            )
        except User.DoesNotExist:
            # Handle the case where the sender or receiver does not exist
            await self.send(text_data=json.dumps({
                'error': 'User does not exist.'
            }))

    async def chat_message(self, event):
        message = event['message']
        sender_id = event['sender']
        print(f'Message received in room {self.room_group_name}: {message} from {sender_id}')
        await self.send(text_data=json.dumps({
            'message': message,
            'sender': sender_id
        }))

    @database_sync_to_async
    def get_sender(self):
        return CustomUser.objects.get(id=self.sender_id)

    @database_sync_to_async
    def get_receiver(self):
        return CustomUser.objects.get(id=self.receiver_id)

    @database_sync_to_async
    def create_message_instance(self, sender, receiver, message):
        return Message.objects.create(sender=sender, receiver=receiver, content=message)
