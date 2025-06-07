from django.shortcuts import render
from apps.env_manager.models import Environment
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from apps.env_manager.services.factory import get_env_service
from django.http import HttpResponse
from django.http import HttpResponseBadRequest

env_service = get_env_service()

@login_required
def dashboard(request):
    environments = Environment.objects.filter(owner=request.user).order_by('-created_at')
    return render(request, 'dashboard.html', {'environments': environments})

@login_required
def create_env(request):
    if request.method == "POST":
        if request.POST.get('name'):
            env = env_service.create_environment(request.POST.get('name'), request.user)
            env.status = "running"
        else:
            return HttpResponseBadRequest("Missing required parameter.")
    return render(request, "partials/_row.html",{"env": env})

@login_required
def delete_env(request, env_id):
    obj = get_object_or_404(Environment, id=env_id)
    if request.method == "POST":
        env_service.delete_environment(obj, request.user)
    return HttpResponse('')

@login_required
def stop_env(request, env_id):
    obj = get_object_or_404(Environment, id=env_id)
    if request.method == "POST":
        env_service.stop_environment(obj, request.user)
        obj.status = "stopped"
    return render(request, "partials/_row.html",{"env": obj})

@login_required
def start_env(request, env_id):
    obj = get_object_or_404(Environment, id=env_id)
    if request.method == "POST":
        env_service.start_environment(obj, request.user)
        obj.status = "running"
    return render(request, "partials/_row.html",{"env": obj})