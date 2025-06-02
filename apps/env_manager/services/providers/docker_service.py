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
        """Creates a dev environment. It stores the environment in the db and also created the docker container

        Args:
            name (str): Name of the environment
            owner (User): Object of the owner of the environment, type User.
        """
        container = None
        try:
            env_id = None
            environment = Environment.objects.create(
                owner=owner,
                name=name,
                image="codercom/code-server:latest",
                status="initializing",
            )
            env_id = environment.id
            router_name = f"code-server-{env_id}"
            service_name = f"code-server-{env_id}"
            middleware_stripprefix = f"code-server-stripprefix-{env_id}"
            middleware_forwardauth = f"code-server-forwardauth-{env_id}"
            path_prefix = f"/environment/{env_id}"

            container = self.client.containers.run(
                image="codercom/code-server:latest",
                command=["--auth=none"],
                labels={
                    "traefik.enable": "true",
                    f"traefik.http.routers.{router_name}.rule": f"PathPrefix(`{path_prefix}`)",
                    f"traefik.http.routers.{router_name}.entrypoints": "web",
                    f"traefik.http.routers.{router_name}.service": service_name,
                    f"traefik.http.services.{service_name}.loadbalancer.server.port": "8080",
                    f"traefik.http.middlewares.{middleware_stripprefix}.stripprefix.prefixes": path_prefix,
                    f"traefik.http.routers.{router_name}.middlewares": f"{middleware_forwardauth},{middleware_stripprefix}",
                    f"traefik.http.middlewares.{middleware_forwardauth}.forwardauth.address": "http://django-docker:8000/auth/",
                    f"traefik.http.middlewares.{middleware_forwardauth}.forwardauth.trustForwardHeader": "true",
                    f"traefik.http.middlewares.{middleware_forwardauth}.forwardauth.authResponseHeaders": "Remote-User"
                },
                network="traefiknet",
                restart_policy={"Name": "unless-stopped"},
                detach=True
            )

            environment.resource_id = container.id
            environment.status = "running"
            environment.save()

            print(f"Container {container.name} started with ID {container.id}")
        except Exception as e:
            print(f"Error creating environment: {e}")
            if container:
                try:
                    print("Cleaning up container...")
                    container.remove(force=True)
                    print(f"Removed container {container.id}")
                except docker.errors.DockerException as cleanup_error:
                    print(f"Failed to clean up container: {cleanup_error}")
            raise
    @transaction.atomic
    def delete_environment(self, environment_id, user):
        """Deletes a environment.

        Args:
            environment_id (int): Id of the environment object.
            user (User): Object of the user which triggered this action

        Raises:
            PermissionError: If the current user has no permissions to delete this environment
            e: Other errors
        """
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