from . import views
from django.urls import path

urlpatterns = [
    path("auth/", views.auth_request, name="auth_request"),
    path("accounts/profile", views.account_profile, name="account_profile"),
]