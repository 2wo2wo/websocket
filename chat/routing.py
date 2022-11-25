from django.urls import re_path,path

from . import consumers

websocket_urlpatterns = [
    path(r"ws/chat/<str:room_name>/", consumers.ChatConsumer.as_asgi()),
]