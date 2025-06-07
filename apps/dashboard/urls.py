from django.urls import path
from . import views



urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('envs/<int:env_id>/delete', views.delete_env, name="delete_env"),
    path('envs/<int:env_id>/stop', views.stop_env, name="stop_env"),
    path('envs/<int:env_id>/start', views.start_env, name="start_env"),
    path('envs/create', views.create_env, name="create_env"),
]
