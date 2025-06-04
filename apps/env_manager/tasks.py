from core.celery import app
from apps.env_manager.services.factory import get_env_service
from django.contrib.auth import get_user_model
from .models import Environment


@app.task
def create_environment(name: str, owner_id):
    User = get_user_model()
    owner = User.objects.get(id=owner_id)
    
    env_service = get_env_service()
    env_service.create_environment(name, owner)
    
@app.task
def delete_environment(environment_id, user_id):
    User = get_user_model()
    user = User.objects.get(id=user_id)
    environment = Environment.objects.get(id=environment_id)
    
    env_service = get_env_service()
    env_service.delete_environment(environment, user)