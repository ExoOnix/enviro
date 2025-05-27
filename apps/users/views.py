from django.http import HttpResponse, HttpResponseForbidden

# Create your views here.
def auth_request(request):
    if request.user.is_authenticated:
        return HttpResponse("Allowed", status=200)
    
    return HttpResponseForbidden("Forbidden: You are not authenticated")