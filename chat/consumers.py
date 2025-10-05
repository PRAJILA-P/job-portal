import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import ChatRoom, ChatMessage
from RECRUITER.models import RecruiterRegister
from USER.models import JobSeeker

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        # Get the chat room
        self.room = await database_sync_to_async(
            lambda: ChatRoom.objects.filter(room_name=self.room_name).first()
        )()
        if not self.room:
            await self.close()
            return

        # Identify user: JobSeeker or Recruiter
        self.job_seeker_id = self.scope['session'].get('jobseeker_id')
        self.recruiter_id = self.scope['session'].get('recruiter_id')

        # Fetch IDs from room safely
        self.job_seeker_id_in_room = await database_sync_to_async(lambda: self.room.job_seeker.id)()
        self.recruiter_id_in_room = await database_sync_to_async(lambda: self.room.recruiter.id)()

        # Only allow users who belong to this chat room
        user_id = self.job_seeker_id or self.recruiter_id
        allowed_users = [self.job_seeker_id_in_room, self.recruiter_id_in_room]
        if user_id not in allowed_users:
            await self.close()
            return

        # Add user to the channel layer group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

        # **Send previous messages to the user**
        previous_messages = await self.get_previous_messages()
        for msg in previous_messages:
            await self.send(text_data=json.dumps({
                'message': msg['message'],
                'sender': msg['sender'],
                'sender_type': msg['sender_type'],
            }))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']

        # Save the message to DB
        saved_message = await self.save_message(message)

        # Send message to room group with sender_type
        await self.channel_layer.group_send(
    self.room_group_name,
    {
        'type': 'chat_message',
        'message': saved_message.message,
        'sender': saved_message.job_seeker_sender.full_name 
                  if saved_message.job_seeker_sender else saved_message.recruiter_sender.company_name,
        'sender_type': 'jobseeker' if saved_message.job_seeker_sender else 'recruiter',
    }
)


    async def chat_message(self, event):
    # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'sender': event['sender'],
            'sender_type': event['sender_type'],  # <--- add this!
        }))


    @database_sync_to_async
    def save_message(self, message):
        room = ChatRoom.objects.get(room_name=self.room_name)

        # Determine sender type
        job_seeker = None
        recruiter = None
        if self.job_seeker_id:
            job_seeker = JobSeeker.objects.get(id=self.job_seeker_id)
        elif self.recruiter_id:
            recruiter = RecruiterRegister.objects.get(id=self.recruiter_id)

        return ChatMessage.objects.create(
            room=room,
            job_seeker_sender=job_seeker,
            recruiter_sender=recruiter,
            message=message
        )
    
    @database_sync_to_async
    def get_previous_messages(self):
        messages = ChatMessage.objects.filter(room=self.room).order_by('timestamp')
        message_list = []
        for msg in messages:
            if msg.job_seeker_sender:
                sender_type = 'jobseeker'
                sender_name = msg.job_seeker_sender.full_name
            else:
                sender_type = 'recruiter'
                sender_name = msg.recruiter_sender.company_name
            message_list.append({
                'message': msg.message,
                'sender': sender_name,
                'sender_type': sender_type  # <-- add this
            })
        return message_list

