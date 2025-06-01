from abc import ABC, abstractmethod

class EnvService(ABC):
    @abstractmethod
    def create_environment(self):
        pass