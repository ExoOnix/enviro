from ..base import EnvService
from django.db import transaction


class DockerService(EnvService):
    @transaction.atomic
    def create_environment(self):
        print("creating service docker")
