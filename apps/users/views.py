from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

# Create your views here.
def auth_request(request):
    if request.user.is_authenticated:
        return HttpResponse("Allowed", status=200)
    
    return HttpResponse("Forbidden: You are not authenticated", status=401)


@login_required
def account_profile(request):
    return HttpResponse(f"Welcome {request.user}!", status=200)
