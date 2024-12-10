import abc


class AbcProperties(abc.ABC):

    @abc.abstractmethod
    def get(self, name: str): ...

    @abc.abstractmethod
    def set(self, name: str, value): ...
