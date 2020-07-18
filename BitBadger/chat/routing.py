# chat/routing.py
from django.urls import re_path, path

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<room_name>\w+)/(?P<receiver_id>\d)/$', consumers.ChatConsumer),
    re_path(r'ws/chat-/(?P<notification>\w+)/$', consumers.NotificationConsumer),
    path('ws/chat/count/messages/', consumers.CountMessagesConsumer),
    path('ws/chat/state/tyiping/', consumers.TypingStateConsumer),
]