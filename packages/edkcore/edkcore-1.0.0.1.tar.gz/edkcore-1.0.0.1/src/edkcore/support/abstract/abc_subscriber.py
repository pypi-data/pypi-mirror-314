import abc

from edkcore.support.abstract.abc_properties import AbcProperties


class AbcSubscriber(abc.ABC):
    def __init__(self, prop: AbcProperties):
        self.prop = prop

    @abc.abstractmethod
    def update(self, *args, **kwargs): ...

