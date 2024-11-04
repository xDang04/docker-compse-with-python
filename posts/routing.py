from django.urls import path
from .consumers import chatConsumer

wsPattern = [
    path('ws/messages/<str:room_name>/', chatConsumer.as_asgi()),
]
