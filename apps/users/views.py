from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
import re

from apps.env_manager.models import Environment

# Create your views here.
def auth_request(request):
    if not request.user.is_authenticated:
        return HttpResponse("Forbidden: You are not authenticated", status=401)
    forwarded_uri = request.META.get('HTTP_X_FORWARDED_URI')
    match = re.search(r'/environment/(\d+)/', forwarded_uri)
    if match:
        env_id = match.group(1)
    else:
        return HttpResponse("Forbidden: You are not authenticated", status=401)
    
    if request.user.environments.filter(id=env_id).exists():
        return HttpResponse("Allowed", status=200)
    
    return HttpResponse("Forbidden: You are not authenticated", status=401)


@login_required
def account_profile(request):
    return HttpResponse(f"Welcome {request.user}!", status=200)
