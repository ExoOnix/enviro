from ..base import EnvService
from django.db import transaction
import docker

# Models
from ...models import Environment
from apps.env_manager.tasks import create_container, delete_container, stop_container, start_container

class DockerService(EnvService):
    def create_environment(self, name: str, owner):
        """Creates and returns the Environment DB object before starting the container."""
        environment = Environment.objects.create(
            owner=owner,
            name=name,
            image="codercom/code-server:latest",
            status="initializing",
        )

        create_container.delay(environment.id)
        
        return environment
    @transaction.atomic
    def delete_environment(self, environment, user):
        """Deletes a environment.

        Args:
            environment (Environment): Object of the environment object.
            user (User): Object of the user which triggered this action

        Raises:
            PermissionError: If the current user has no permissions to delete this environment
            e: Other errors
        """
        try:            
            if environment.owner != user:
                raise PermissionError("You do not have permission to delete this environment.")

            
            delete_container.delay(environment.id)
        except Exception as e:
            raise e
    @transaction.atomic
    def stop_environment(self, environment, user):
        """Pauses a environment using the docker api

        Args:
            environment (Environment): Environment instance
            user (User): User instance
        """
        try:            
            if environment.owner != user:
                raise PermissionError("You do not have permission to delete this environment.")
            
            stop_container.delay(environment.id)
        except Exception as e:
            raise e
    @transaction.atomic
    def start_environment(self, environment, user):
        """Starts a environment using the docker api

        Args:
            environment (Environment): Environment instance
            user (User): User instance
        """
        try:            
            if environment.owner != user:
                raise PermissionError("You do not have permission to delete this environment.")
            
            start_container.delay(environment.id)
        except Exception as e:
            raise e