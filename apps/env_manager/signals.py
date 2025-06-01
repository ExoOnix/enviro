# code
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from .models import Environment
import docker

@receiver(pre_delete, sender=Environment) 
def create_profile(sender, instance, **kwargs):
    try:
        client = docker.from_env()
        
        container = client.containers.get(instance.resource_id)
        
        container.stop()
        container.remove()
    except docker.errors.NotFound:
        print(f"Container with id {instance.resource_id} not found, removing Environment record.")
    except Exception as e:
        print(f"Error removing environment: {e}")
        raise e