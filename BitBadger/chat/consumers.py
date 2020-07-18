# chat/consumers.py
from asgiref.sync import async_to_sync
from django.contrib.auth import get_user_model
import json
from channels.generic.websocket import WebsocketConsumer
from django.shortcuts import get_object_or_404

from .models import Message, MessageUserStatus

User = get_user_model()

class ChatConsumer(WebsocketConsumer):

    def new_message(self, data):
        author = data['from']
        author_user = User.objects.filter(username = author)[0]
        message = Message.objects.create(author = author_user, content = data['message'], room_name = self.room_name)
        receiver = User.objects.get(pk = self.receiver_id)
        
        message_status = MessageUserStatus.objects.create(message_receiver = receiver, message = message, is_read = False)
        
        content = {
            'command' : 'new_message',
            'messages' : self.message_to_json(message)
        }
        
        return self.send_chat_message(content)
    
    def messages_to_json(self, messages):
        result = []
        for message in messages:
            result.append(self.message_to_json(message))
            
        return result
            
    def message_to_json(self, message):
        return {
            'author' : message.author.username,
            'content' : message.content,
            'timestamp' : str(message.timestamp)
        }
    
    commands = {
        'new_message' : new_message
    }
    
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.receiver_id = self.scope['url_route']['kwargs']['receiver_id']
                
        self.room_group_name = 'chat_%s' % self.room_name
        
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()
    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )
    # Receive message from WebSocket
    def receive(self, text_data):
        data = json.loads(text_data)
        
        self.commands[data['command']](self, data)
        
    def send_chat_message(self, message):
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )
    
    def send_message(self, message):
        self.send(text_data = json.dumps(message))
    
    def chat_message(self, event):
        message = event['message']
        # Send message to WebSocket
        
        self.send(text_data = json.dumps(message))
                

class NotificationConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['notification']
        self.room_group_name = 'chat_%s' % self.room_name
        
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        
        self.accept()
        
    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )
        
    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message_received = text_data_json['message_received']
        room_name_id = text_data_json['room_name_id']
        
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message_received': message_received,
                'room_name_id' : room_name_id
            }
        )
        
    # Receive message from room group
    def chat_message(self, event):
        message_received = event['message_received']
        room_name_id = event['room_name_id']
        
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message_received': message_received,
            'room_name_id' :room_name_id
        }))
        
        
class CountMessagesConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = 'counter'
        self.room_group_name = 'chat_%s' % self.room_name
        
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        
        self.accept()
        
    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )
        
    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        receiver_id = text_data_json['receiver_id']
        room_name = text_data_json['room_name']
        user_id = text_data_json['user_id']
        
        state = "update"
        
        print(user_id, ' - ', receiver_id)
        
        if user_id == receiver_id:
            this_user = get_object_or_404(User, pk = int(user_id))
            
            unread_messages = MessageUserStatus.objects.filter(message_receiver = this_user, message__room_name = room_name, is_read = False)
        
            for message in unread_messages:#mark all unread messages a read
                message.is_read = True
                message.save()
                
            state = "updated"
        
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type' : 'count_message',
                'receiver_id': receiver_id,
                'room_name' : room_name,
                'user_id' : user_id,
                'state' : state
            }
        )
        
    # Receive message from room group
    def count_message(self, event):
        receiver_id = event['receiver_id']
        room_name = event['room_name']
        state = event['state']
        
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message_count': self.countUnreadMessages(receiver_id, room_name),
            'room_name' :room_name,
            'receiver_id' : receiver_id,
            'state' : state
        }))
        
    def countUnreadMessages(self, receiver_id, room_name):
        receiver = User.objects.get(pk = receiver_id)
        all_unread_messges = MessageUserStatus.objects.filter(message_receiver = receiver, message__room_name = room_name, is_read = False)
        return len(all_unread_messges)
    
class TypingStateConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = 'state'
        self.room_group_name = 'chat_%s' % self.room_name
        
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        
        self.accept()
       
    def disconnect(self,close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )
    
    def receive(self, text_data):
        data = json.loads(text_data)
        receiver = data['receiver_id']
        sender = data['sender_id']
        current_room_name = data['current_room_name']
        
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type' : 'state',
                'receiver_id' : receiver,
                'sender_id' : sender,
                'current_room_name' : current_room_name
            }
        )
    
    def state(self, event):
        receiver = event['receiver_id']
        sender = event['sender_id']
        current_room_name = event['current_room_name']
        
        self.send(text_data = json.dumps({
            'receiver' : receiver,
            'sender' : sender,
            'current_room_name' : current_room_name
        }))