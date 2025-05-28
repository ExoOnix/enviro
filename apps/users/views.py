from django.http import HttpResponse

# Create your views here.
def auth_request(request):
    if request.user.is_authenticated:
        return HttpResponse("Allowed", status=200)
    
    return HttpResponse("Forbidden: You are not authenticated", status=401)

def account_profile(request):
    if request.user.is_authenticated:
        return HttpResponse(f"Welcome {request.user.username}!", status=200)
    
    return HttpResponse("Forbidden: You are not authenticated", status=401)