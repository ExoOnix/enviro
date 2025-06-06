from django.shortcuts import render
from .models import Environment
from django.http import HttpResponseNotFound

def waiting_room(request, number: int):
    env = Environment.objects.filter(pk=number).first()
    if env is None:
        return HttpResponseNotFound("Environment does not exist")
    else:
        return render(request, 'waiting_room.html', {'environment': env})