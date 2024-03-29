import json
from .message import save_message
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from datetime import datetime


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = str(self.scope["url_route"]["kwargs"]['path_to_chat'])

        self.room_group_name = "chat_%s" % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name, self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name, self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        user = text_data_json["user_id"]
        time = str(datetime.now())
        unique_room = self.scope["url_route"]["kwargs"]['path_to_chat']
        await save_message(unique_room, user, message)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat_message",
                                   "user": user,
                                   "message": message,
                                   "time": time}
        )

    # Receive message from room group
    async def chat_message(self, event):
        user_id = event['user']
        message = event["message"]
        time = event['time']
        #
        # Send message to WebSocket
        # print(event)

        await self.send(text_data=json.dumps({
            'user_id': user_id,
            "message": message,
            'time': time
        }))
