from django.contrib import admin

from .models import Message, MessageUserStatus

admin.site.register(Message)
admin.site.register(MessageUserStatus)