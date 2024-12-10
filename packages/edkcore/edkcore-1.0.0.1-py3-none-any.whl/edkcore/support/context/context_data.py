import abc

from edkcore.support.abstract.abc_persistent_device import AbcPersistentDevice
from edkcore.support.context.data_info import DataInfo
from edkcore.support.properties.context_data_properties import ContextDataProperties


class ContextData(abc.ABC):

    def __init__(self, context_action, properties: ContextDataProperties = ContextDataProperties()):
        self.content = dict()
        self._context_action = context_action
        self._props = properties

    @property
    def persistents(self):
        """
        返回 ContextData 使用持久化存储
        :return:
        :rtype:
        """
        return self._props.get("persistents")

    @property
    def datas_info(self) -> list[DataInfo]:
        return self._props.datas_info

    def update(self, value):
        self.content.update(value)

    def get(self, key):
        return self.content.get(key)

    @abc.abstractmethod
    def set(self, name, value): ...

    @abc.abstractmethod
    def persistence(self, persistent: AbcPersistentDevice):
        """
        把数据转化为持久化的格式，存储在存储容器中
        :return:
        :rtype:
        """
        ...

    def serialization(self, persistent: AbcPersistentDevice):
        self._serialize(persistent)
        return self

    @abc.abstractmethod
    def _serialize(self, persistent: AbcPersistentDevice):
        """
        把数据读去出来，转为对象供使用
        :param persistent:
        :type persistent:
        :return:
        :rtype:
        """
        ...
