from django import template
from datetime import datetime

from chat.models import Message, MessageUserStatus

register = template.Library()

@register.simple_tag(takes_context=True)

def create_room_name(context, receiver_id):
    request = context.get("request")
    user_id = request.user.id

    if user_id == min(int(receiver_id), int(user_id)):
        room_name = str(user_id)+'_'+str(receiver_id)
    else:
        room_name =  str(receiver_id)+'_'+str(user_id)
        
    unread_messages = MessageUserStatus.objects.filter(message_receiver = request.user, message__room_name = room_name, is_read = False)
    
    try:
        latest_text = Message.objects.filter(room_name = room_name).order_by('-timestamp')[:1]
        latest_text = latest_text[0]
    except:
        latest_text = ""
        
    data = {
        'room_name' : room_name,
        'latest_text' : latest_text,
        'unread_messages' : len(unread_messages)
    }
    return data

@register.simple_tag()
def generate_date(date):
    if(date):
        dateobj = date
        today =datetime.today()
        
        date = date.strftime('%m/%d/%Y')
        
        yesterday = datetime(int(today.strftime('%Y')),int(today.strftime('%m')),int(int(today.strftime('%d')) - 1 ))
        
        today = today.strftime('%m/%d/%Y')
        
        if(datetime.strptime(date, '%m/%d/%Y') == datetime.strptime(today, '%m/%d/%Y')):
            return "Today,"
        elif(yesterday == datetime.strptime(date, '%m/%d/%Y')):
            return "Yesterday,"
        else:
            return None
    else:
        return None
    
