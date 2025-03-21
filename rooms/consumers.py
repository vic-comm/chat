# creating consumer
import json
# import django
# django.setup()
from .models import Rooms, Message
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from django.contrib.auth.models import User
import base64
from django.core.files.base import ContentFile

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name= 'chat_%s' % self.room_name
        print(self.room_name)
        await self.channel_layer.group_add(
            # self.room_name,
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data.get('message', '')
        file_data = data.get('file', None)
        file_name = data.get('filename', 'uploaded_file')
        username = data['username']
        room = data['room']
            
        
        chat_msg = await self.save_message(username, room, message, file_data, file_name)
        await self.channel_layer.group_send(
            self.room_group_name, {
                'type':'chat_message',
                'message':message,
                'username':username,
                'room':room,
                'file_url': chat_msg.file.url if chat_msg.file else None
                # "filename": file_name if chat_msg.file else None,
            }
        )

        print(message)

    async def chat_message(self, event):
        message = event["message"]
        username = event["username"]
        room = event["room"]
        file_url = event.get('file_url', None)
        # file_name = event.get('file_name', None)

        await self.send(text_data=json.dumps({
            "message": message,
            "username": username,
            "room": room,
            'file_url' : file_url
        }))


    @sync_to_async
    def save_message(self, username, room, message, file_data=None, file_name='uploaded_file'):
        user = User.objects.get(username=username)
        room = Rooms.objects.get(slug=room)

        if file_data:
            # file_name = data.get('filename', 'uploaded file')
            # decoded_file = b64.bas64decode(file_data)
            decoded_file = base64.b64decode(file_data)  # Correct
            chat_msg = Message(user=user, room=room)
            chat_msg.file.save(file_name, ContentFile(decoded_file), save=True)
        else:
            chat_msg = Message.objects.create(user=user, content=message, room=room)

    
        print(f"Message saved: {chat_msg.content if message else file_name}")  # Debugging print
        return chat_msg
        # Message.objects.create(user=user, room=room, content=message)