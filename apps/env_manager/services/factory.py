from .providers.docker_service import DockerService
from django.conf import settings


def get_env_service():
    services = {
        'docker': DockerService,
    }
    service_class = services.get(settings.ENV_PROVIDER)
    if not service_class:
        raise ValueError(f"Unsupported provider: {settings.ENV_PROVIDER}")
    return service_class()
