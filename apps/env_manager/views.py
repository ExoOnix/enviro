from django.shortcuts import render
from .models import Environment
from django.http import HttpResponseNotFound, HttpResponse

def waiting_room(request, number: int):
    env = Environment.objects.filter(pk=number).first()
    if env is None:
        return HttpResponseNotFound("Environment does not exist")
    elif env.status == "stopped":
        return HttpResponse("Environment is stopped")
    else:
        return render(request, 'waiting_room.html', {'environment': env})