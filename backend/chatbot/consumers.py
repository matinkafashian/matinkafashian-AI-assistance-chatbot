import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import ChatSession, Message
from .ai_service import AIService


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.session_id = self.scope['url_route']['kwargs']['session_id']
        self.room_group_name = f'chat_{self.session_id}'

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

        # Get or create session
        session = await self.get_or_create_session()

        # Save user message
        user_message = await self.save_message(session, 'user', message)

        # Send user message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'message_type': 'user',
                'message_id': user_message.id
            }
        )

        # Get AI response
        ai_response = await self.get_ai_response(message)

        # Save AI response
        ai_message = await self.save_message(session, 'assistant', ai_response['response'])

        # Send AI response to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': ai_response['response'],
                'message_type': 'assistant',
                'message_id': ai_message.id,
                'response_time': ai_response['response_time'],
                'sources': ai_response.get('sources', [])
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'message_type': event['message_type'],
            'message_id': event['message_id'],
            'response_time': event.get('response_time'),
            'sources': event.get('sources', [])
        }))

    @database_sync_to_async
    def get_or_create_session(self):
        session, created = ChatSession.objects.get_or_create(
            session_id=self.session_id,
            defaults={'is_active': True}
        )
        return session

    @database_sync_to_async
    def save_message(self, session, message_type, content):
        return Message.objects.create(
            session=session,
            message_type=message_type,
            content=content
        )

    @database_sync_to_async
    def get_ai_response(self, message):
        ai_service = AIService()
        return ai_service.generate_response(message, self.session_id)
