from edkcore.support.enums.action_enum import ActionEnum
from edkcore.support.properties.context_properties import ContextProperties


class RestoreProperties(ContextProperties):
    def __init__(self):
        super().__init__()

    @property
    def store(self): return self.get('store', [])

    @store.setter
    def store(self, value):
        if not self.store: self.set("store", [value])
        else: self._data["store"].append(value)

    def property_type(self) -> ActionEnum: return ActionEnum.Restore


