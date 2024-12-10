import abc

from edkcore.support.context.context_action_data import ContextActionData
from edkcore.support.context.data_info import DataInfo


class AbcPersistence(abc.ABC):
    def __init__(self, context_action_data: ContextActionData, persistent):
        self.context_action_data = context_action_data
        self.persistent = persistent

    @abc.abstractmethod
    def persistence(self, data_info: DataInfo, cur_data, his_data: list): ...

    def ins(self):
        return self.persistent.ins()
