from abc import ABC, abstractmethod

class EnvService(ABC):
    @abstractmethod
    def create_environment(self, name: str, owner):
        pass
    @abstractmethod
    def delete_environment(self, environment, user):
        pass
    @abstractmethod
    def stop_environment(self, environment, user):
        pass