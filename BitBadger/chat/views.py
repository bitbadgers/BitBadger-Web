# chat/views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.utils.safestring import mark_safe
import json
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.http import Http404
from datetime import datetime

from DevsPlatform.views import ContextBuilder
from .models import MessageUserStatus, Message


@login_required
def index(request):
    return render(request, 'chat/index.html', ContextBuilder(request))

@login_required
def room(request, room_name = None):
    def fetch_messages(room):       
        messages = Message.last_30_messages(room)
        return messages

    if room_name:
        try:
            room_name.split('_')[1]
            receiver_id = fetch_receiver(room_name, request.user.id)
        except:
            raise Http404
        
        unread_messages = MessageUserStatus.objects.filter(message_receiver = request.user, message__room_name = room_name, is_read = False)
        
        for message in unread_messages:#mark all unread messages a read
            message.is_read = True
            message.save()
        
        
        context = ContextBuilder(request,
                    room_name= room_name,
                    room_name_json = mark_safe(json.dumps(room_name)),
                    username = mark_safe(json.dumps(request.user.username)),
                    users = User.objects.all(),
                    receiver = get_object_or_404(User, pk = int(receiver_id)),
                    preload_messages = fetch_messages(room_name),
                )
        return render(request, 'chat/chat.html', context)
    else:
        context = ContextBuilder(request,
                    username = mark_safe(json.dumps(request.user.username)),
                    users = User.objects.all()
                )
        
        return render(request, 'chat/room.html', context)
                    
def fetch_receiver(room_name, current_user):
    sender_receiver = room_name.split('_')
    current_user = str(current_user)
    
    if current_user in sender_receiver:
        user_index = sender_receiver.index(current_user)
        if user_index == 0:
            return sender_receiver[1]
        else:
            return sender_receiver[0]
    else:
        return Http404
    