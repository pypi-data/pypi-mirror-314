import abc


class AbcCallBack(abc.ABC):
    @abc.abstractmethod
    def call_back(self): ...
