import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import ChatOneToOne, Message
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from django.db import models
from datetime import datetime

@database_sync_to_async
def get_username_by_id(sender_id):
    try:
        user = User.objects.get(id=sender_id)
        return user.username  # Hoặc bạn có thể lấy tên người dùng khác nếu muốn
    except User.DoesNotExist:
        return None
class ChatConsumer(AsyncWebsocketConsumer):
   
    async def connect(self):
        # Dùng chat_id từ URL để xác định nhóm
        self.chat_id = self.scope['url_route']['kwargs']['chat_id']
        self.room_group_name = f'chat_{self.chat_id}'

        # Thêm vào group để nhận tin nhắn
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()
        
        
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message_content = text_data_json['message']
        sender_id = text_data_json['sender_id']

        # Lấy tên người gửi
        sender_username = await get_username_by_id(sender_id)

        # Kiểm tra và lưu tin nhắn vào DB
        chat = await self.get_chat()
        if chat:
            time_stamp = datetime.now().strftime('%H:%M')
            await self.save_message(chat, sender_id, message_content,time_stamp)

            # Gửi tin nhắn đến tất cả các thành viên trong nhóm
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message_content,
                    'sender_username': sender_username,
                    'time_stamp': time_stamp
                }
            )

    async def chat_message(self, event):
        # Lấy message và sender từ event
        message = event['message']
        sender_username = event['sender_username']
        time_stamp = event['time_stamp']
        # Gửi tin nhắn tới WebSocket client
        await self.send(text_data=json.dumps({
            'message': message,
            'sender_username': sender_username,
            'time_stamp': time_stamp
        }))
    
    @database_sync_to_async
    def get_chat(self):
        # Tìm cuộc trò chuyện dựa trên chat_id
        try:
            return ChatOneToOne.objects.get(id=self.chat_id)
        except ChatOneToOne.DoesNotExist:
            return None

    @database_sync_to_async
    def get_messages(self, chat):
        return chat.messages.all()  # Lấy tất cả tin nhắn từ cuộc trò chuyện

    @database_sync_to_async
    def save_message(self, chat, sender_id, content,time_stamp):
        sender = User.objects.get(id=sender_id)
        Message.objects.create(chat=chat, sender=sender, content=content,time_stamp=time_stamp)