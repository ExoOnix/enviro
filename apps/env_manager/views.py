from django.shortcuts import render
from .models import Environment
from django.http import HttpResponseNotFound, HttpResponse
from apps.home import views as home_views
from django.conf import settings


def waiting_room(request, number: int):
    env = Environment.objects.filter(pk=number).first()
    if env is None:
        return HttpResponseNotFound("Environment does not exist")
    elif env.status == "stopped":
        return HttpResponse("Environment is stopped")
    else:
        return render(request, 'waiting_room.html', {'environment': env})

def loading_room(request):
    host = request.get_host().split(':')[0]  # Remove port if present
    hostname = settings.HOSTNAME

    if host.endswith(hostname):
        subdomain_part = host[:-len(hostname)].rstrip('.')
        subdomain_levels = subdomain_part.split('.')
        if subdomain_levels and subdomain_levels[-1].startswith('env-'):
            return render(request, 'waiting_room.html')

    return home_views.home(request)