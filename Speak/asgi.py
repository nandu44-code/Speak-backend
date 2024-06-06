"""
ASGI config for Speak project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os
from django.urls import path
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from chat.consumers import ChatConsumer
from django.core.asgi import get_asgi_application
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Ensure the settings module is specified

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Speak.settings')

# Initialize Django ASGI application early to ensure the AppRegistry is populated correctly.
django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    'http': django_asgi_app,
    'websocket': AuthMiddlewareStack(
        URLRouter(
            [
                path("ws/chat/<int:sender_id>/<int:receiver_id>/", ChatConsumer.as_asgi()),
            ]
        )
    ),
})
