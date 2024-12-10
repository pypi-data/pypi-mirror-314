import abc

from edkcore.support.context.context_action_data import ContextActionData
from edkcore.support.context.data_info import DataInfo


class AbcSerialize(abc.ABC):
    def __init__(self, context_action_data: ContextActionData, data_info: DataInfo, persistent):
        self.context_action_data = context_action_data
        self.data_info = data_info
        self.persistent = persistent

    @abc.abstractmethod
    def serializing(self) -> list:  ...

    def serialize(self):
        for data in (self.serializing() or []):
            self.context_action_data.set(self.data_info.name, data)

    def ins(self): return self.persistent.ins()
