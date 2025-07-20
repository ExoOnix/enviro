from django.shortcuts import render
from apps.env_manager.models import Environment, EnvironmentTemplate
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from apps.env_manager.services.factory import get_env_service
from django.http import HttpResponseBadRequest
from django.conf import settings
from django_ratelimit.decorators import ratelimit
from django.http import JsonResponse

# Services
from .services import env_key

env_service = get_env_service()

@login_required
def dashboard(request):
    environments = Environment.objects.filter(owner=request.user).order_by('-created_at')
    env_tempates = EnvironmentTemplate.objects.all()
    env_limit = settings.ENV_LIMITS
    return render(request, 'dashboard.html', {'environments': environments, 'environment_limit': env_limit, 'env_tempates': env_tempates})

@login_required
@ratelimit(key='user', rate='1/15s', block=False)
def create_env(request):
    was_limited = getattr(request, 'limited', False)
    if was_limited:
        response = JsonResponse({'error': 'Rate limit exceeded.'}, status=429)
        response['HX-Trigger'] = '{"showToast": "Rate limit exceeded. Please wait before trying again."}'
        return response
    if request.method == "POST":
        env_count = Environment.objects.filter(owner=request.user).count()
        env_limit = settings.ENV_LIMITS
        if env_limit != 0 and env_count >= env_limit:
            return HttpResponseBadRequest("Environment limit reached.")
        if request.POST.get('name') and request.POST.get('selectedTemplate'):
            if request.POST.get('selectedTemplate') == "Blank":
                env = env_service.create_environment(request.POST.get('name'), request.user)
                env.status = "running"
                env_count += 1
            else:
                env_template = EnvironmentTemplate.objects.get(id=int(request.POST.get('selectedTemplate')))
                env_template_image = env_template.image
                env = env_service.create_environment(request.POST.get('name'), request.user, env_template_image)
                env.status = "running"
                env_count += 1
        else:
            return HttpResponseBadRequest("Missing required parameter.")
        return render(request, "partials/_row.html", {"env": env, 'environment_limit': env_limit, 'env_count': env_count})

@login_required
def delete_env(request, env_id):
    obj = get_object_or_404(Environment, id=env_id)
    env_count = Environment.objects.filter(owner=request.user).count()
    env_limit = settings.ENV_LIMITS

    if request.method == "POST":
        env_service.delete_environment(obj, request.user)
        env_count -= 1
    return render(request, 'partials/_delete_oob.html', {'environment_limit': env_limit, 'env_count': env_count})

@login_required
@ratelimit(group='env_action', key=env_key, rate='1/30s', block=False)
def stop_env(request, env_id):
    was_limited = getattr(request, 'limited', False)
    if was_limited:
        response = JsonResponse({'error': 'Rate limit exceeded.'}, status=429)
        response['HX-Trigger'] = '{"showToast": "Rate limit exceeded. Please wait before trying again."}'
        return response
    obj = get_object_or_404(Environment, id=env_id)
    env_count = Environment.objects.filter(owner=request.user).count()
    env_limit = settings.ENV_LIMITS
    if request.method == "POST":
        env_service.stop_environment(obj, request.user)
        obj.status = "stopped"
    return render(request, "partials/_row.html",{"env": obj, 'environment_limit': env_limit, 'env_count': env_count})

@login_required
@ratelimit(group='env_action', key=env_key, rate='1/30s', block=False)
def start_env(request, env_id):
    was_limited = getattr(request, 'limited', False)
    if was_limited:
        response = JsonResponse({'error': 'Rate limit exceeded.'}, status=429)
        response['HX-Trigger'] = '{"showToast": "Rate limit exceeded. Please wait before trying again."}'
        return response
    obj = get_object_or_404(Environment, id=env_id)
    env_count = Environment.objects.filter(owner=request.user).count()
    env_limit = settings.ENV_LIMITS
    if request.method == "POST":
        env_service.start_environment(obj, request.user)
        obj.status = "running"
    return render(request, "partials/_row.html",{"env": obj, 'environment_limit': env_limit, 'env_count': env_count})