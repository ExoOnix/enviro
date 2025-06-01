from ..base import EnvService
from django.db import transaction
import docker

# Models
from ...models import Environment

class DockerService(EnvService):
    def __init__(self):
        self.client = docker.from_env()
    @transaction.atomic
    def create_environment(self, name: str, owner):
        container = None
        try:
            container = self.client.containers.run(
                image="codercom/code-server:latest",
                command=["--auth=none"],
                labels={
                    "traefik.enable": "true",
                    "traefik.http.routers.code-server.rule": "PathPrefix(`/code`)",
                    "traefik.http.routers.code-server.entrypoints": "web",
                    "traefik.http.services.code-server.loadbalancer.server.port": "8080",
                    "traefik.http.middlewares.code-server-stripprefix.stripprefix.prefixes": "/code",
                    "traefik.http.routers.code-server.middlewares": "code-server-stripprefix,code-server-forwardauth",
                    "traefik.http.middlewares.code-server-forwardauth.forwardauth.address": "http://django-docker:8000/auth/",
                    "traefik.http.middlewares.code-server-forwardauth.forwardauth.trustForwardHeader": "true",
                    "traefik.http.middlewares.code-server-forwardauth.forwardauth.authResponseHeaders": "Remote-User"
                },
                network="traefiknet",
                restart_policy={"Name": "unless-stopped"},
                detach=True
            )

            environment = Environment.objects.create(
                owner=owner,
                name=name,
                image=container.image.id,
                status="running",
                resource_id=container.id,
            )

            print(f"Container {container.name} started with ID {container.id}")
        except Exception as e:
            print(f"Error creating environment: {e}")
            # Cleanup container if it was created
            if container:
                try:
                    print("Cleaning up container...")
                    container.remove(force=True)
                    print(f"Removed container {container.id}")
                except DockerException as cleanup_error:
                    print(f"Failed to clean up container: {cleanup_error}")
            raise
    @transaction.atomic
    def delete_environment(self, environment_id, user):
        try:
            environment = Environment.objects.get(id=environment_id)
            
            if environment.owner != user:
                raise PermissionError("You do not have permission to delete this environment.")

            
            container = self.client.containers.get(environment.resource_id)
            
            container.stop()
            container.remove()
            
            environment.delete()
        except docker.errors.NotFound:
            print(f"Container with id {environment.resource_id} not found, removing Environment record.")
            environment.delete()
        except Exception as e:
            print(f"Error removing environment: {e}")
            raise e