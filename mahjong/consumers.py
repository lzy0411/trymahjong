# chat/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))

class JoinRoomConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        print("!!!!!!!!!  CONNECT !!!!!!!!!!!!!!")
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        print("!!!!!!!!!  ready to accept !!!!!!!!!!!!!!")
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        print("!!!!!!!!!  DISCONNECT !!!!!!!!!!!!!!")
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        print(text_data_json)
        user_num = text_data_json['user_num']
        user_id = text_data_json['user_id']
        user_name = text_data_json['user_name']
        message = text_data_json['message']


        # Send message to room group
        print("!!!!!!!!!  receive !!!!!!!!!!!!!!")
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'user_num': user_num,
                'user_id': user_id,
                'user_name': user_name,
                'message': message,
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        
        user_num = event['user_num']
        user_id = event['user_id']
        user_name = event['user_name']
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'user_num': user_num,
            'user_id': user_id,
            'message': message,
            'user_name': user_name,
        }))

class GameConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print("!!!!!!!!!  CONNECT !!!!!!!!!!!!!!")
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'game_%s' % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        print("!!!!!!!!!  DISCONNECT !!!!!!!!!!!!!!")
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        print("!!!!!!!!!  receive !!!!!!!!!!!!!!")
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'game_message',
                'message': message
            }
        )

    # Receive message from room group
    async def game_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))