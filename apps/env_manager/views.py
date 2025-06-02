from django.shortcuts import render

def waiting_room(request, number: int):
    return render(request, 'waiting_room.html')