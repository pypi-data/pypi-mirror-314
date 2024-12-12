from abc import ABC, abstractmethod


class BaseAdapter(ABC):
    _adapters: dict[str, set] = dict()

    def __init__(self):
        self.__view = None

    @abstractmethod
    async def get_view(self):
        ...

    @property
    def view(self):
        return self.__view

    @classmethod
    def get_adapters(cls) -> list:
        return cls._adapters.get(cls.__name__, [])

    @classmethod
    def add_adapter(cls, service):
        group = cls._adapters.get(cls.__name__, None)
        if group:
            group.add(service)
        else:
            cls._adapters[cls.__name__] = {service, }

    @classmethod
    def remove_adapter(cls, service):
        group = cls._adapters.get(cls.__name__, None)
        if group:
            group.remove(service)
