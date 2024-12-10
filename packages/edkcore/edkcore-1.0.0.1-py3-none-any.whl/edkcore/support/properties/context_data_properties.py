from edkcore.support.abstract.abc_properties import AbcProperties
from edkcore.support.context.data_info import DataInfo
from edkcore.support.enums.action_enum import ActionEnum
from edkcore.support.enums.persistent_enum import PersistentEnum
from edkcore.support.persistents.persistent_device_info import PersistentDeviceInfo


class ContextDataProperties(AbcProperties):
    def __init__(self):
        self._props = dict(persistents=[], datas=[])
        # self.memory_persistent()

    def get(self, name: str):
        return self._props.get(name)

    def set(self, name: str, value):
        self._props[name] = value

    @property
    def persistents(self) -> list[PersistentDeviceInfo]:
        return self.get("persistents")

    @property
    def datas_info(self) -> list[DataInfo]:
        return self.get("datas")

    def add_persistent(self, persistent_device: PersistentDeviceInfo):
        self._props["persistents"].append(persistent_device)

    def add_data(self, data_info: DataInfo):
        self._props["datas"].append(data_info)

    def property_type(self) -> ActionEnum: return ActionEnum.ContextData

    @property
    def clazz(self):
        return self.get("class")

    @clazz.setter
    def clazz(self, value):
        self.set("class", value)

    @property
    def path(self):
        return self.get("path")

    @path.setter
    def path(self, value):
        self.set("path", value)
