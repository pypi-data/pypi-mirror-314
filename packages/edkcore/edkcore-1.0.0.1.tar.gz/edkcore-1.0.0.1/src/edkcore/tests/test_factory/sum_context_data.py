from edkcore.support.abstract.abc_persistent_device import AbcPersistentDevice
from edkcore.support.context.context_data import ContextData

from edkcore.support.persistents.dict_persistent_device import DictPersistentDevice
from edkcore.support.persistents.persistent_device_info import PersistentDeviceInfo
from edkcore.support.properties.context_data_properties import ContextDataProperties


class SumContextData(ContextData):
    def set(self, name, value):
        pass

    def __init__(self, context_action, properties=ContextDataProperties()):
        super().__init__(context_action, properties)
        self.content["count"] = 0
        self._props.add_persistent(PersistentDeviceInfo(name="Memory", clazz=DictPersistentDevice, configuration=dict()))

    def persistence(self, persistent: AbcPersistentDevice):
        if persistent.name == "Memory":
            persistent.ins().update(self.content)

    def _serialize(self, persistent: AbcPersistentDevice):
        if persistent.name == "Memory":
            self.content = persistent.ins()

    def add(self):
        number = self.content.get(self._context_action.index(0).uid).get("Number")
        self.content["count"] += number

    def count(self):
        return self.content["count"]
