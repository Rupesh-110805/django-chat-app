from channels.generic.websocket import AsyncWebsocketConsumer
import json
from asgiref.sync import sync_to_async
from django.contrib.auth.models import User
from .models import ChatRoom,ChatMessage
class ChatConsumer(AsyncWebsocketConsumer):
    
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        
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
        print(f"Received data: {text_data}")  # Debug print
        data = json.loads(text_data)
        message = data['message']
        username = data['username']
        room = data['room']
        
        print(f"Parsed - Message: {message}, Username: {username}, Room: {room}")  # Debug print
        
        await self.channel_layer.group_send(
            self.room_group_name, {
                'type': 'chat_message',
                'message': message,
                'username': username,
                'room': room,
            }
        )
        
        await self.save_message(username, room, message)
        
    async def chat_message(self, event):
        message = event['message']
        username = event['username']
        room = event['room']
        
        print(f"Broadcasting message: {message} from {username} in {room}")  # Debug print
        
        await self.send(text_data=json.dumps({
            'message': message,
            'username': username,
            'room': room,
        }))
    
    @sync_to_async 
    def save_message(self, username, room, message):
        try:
            user = User.objects.get(username=username)
            room_obj = ChatRoom.objects.get(slug=room)
            ChatMessage.objects.create(user=user, room=room_obj, message_content=message)
            print(f"Message saved successfully: {message}")
        except Exception as e:
            print(f"Error saving message: {e}")
    