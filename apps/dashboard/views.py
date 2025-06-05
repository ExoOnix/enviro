from django.shortcuts import render
from apps.env_manager.models import Environment
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    environments = Environment.objects.filter(owner=request.user)
    return render(request, 'dashboard.html', {'environments': environments})