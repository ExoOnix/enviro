from abc import ABC, abstractmethod

class EnvService(ABC):
    @abstractmethod
    def create_environment(self, name: str, owner):
        pass
    @abstractmethod
    def delete_environment(self, environment_id, user):
        pass