from abc import ABC, abstractmethod


class ExternalService(ABC):
    _instances = set()

    def __init__(self):
        ExternalService.add_service(self)

    @abstractmethod
    async def execute(self):
        pass

    @classmethod
    async def get_instances(cls):
        return [instance for instance in cls._instances if isinstance(instance, cls)]

    @classmethod
    def add_service(cls, service):
        cls._instances.add(service)

    @classmethod
    def remove_service(cls, service):
        cls._instances.remove(service)
