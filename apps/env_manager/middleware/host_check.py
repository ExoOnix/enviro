from django.conf import settings
from django.shortcuts import redirect
from django.urls import reverse, resolve
from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import render


class HostnameMiddleware(MiddlewareMixin):
    def process_request(self, request):
        current_host = request.get_host().split(':')[0]  # Remove port if present
        expected_host = settings.HOSTNAME

        # Skip auth request paths
        if resolve(request.path_info).url_name == "auth_request":
            return self.get_response(request)


        # Skip if it's already the waiting room path (avoid infinite loop)
        if resolve(request.path_info).url_name == "waiting_room":
            return None

        if current_host != expected_host:
            # Show waiting room
            return render(request, 'waiting_room.html')
        
        return None  # Continue processing
