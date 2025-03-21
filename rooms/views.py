from django.shortcuts import render
from .models import Rooms, Message
from django.contrib.auth.decorators import login_required
# Create your views here.
@login_required
def rooms(request):
    rooms = Rooms.objects.all()
    return render (request, 'rooms/rooms.html', {'rooms':rooms})

@login_required
def room(request, slug):
    room = Rooms.objects.get(slug=slug)
    messages = Message.objects.filter(room=room)[:25]
    for i in messages:
        print(i.content)
    return render (request, 'rooms/room1.html', {'room':room, 'messages':messages})