from django.shortcuts import render


def index(request):
    return render(request, 'renga/index.html', {})


def room(request, room_name):
    return render(request, 'renga/room.html', {'room_name': room_name})
