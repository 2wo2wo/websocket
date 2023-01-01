from django.urls import re_path,path

from . import consumers

websocket_urlpatterns = [
    path("ws/chat/<uuid:path_to_chat>/", consumers.ChatConsumer.as_asgi()),
]