from edkcore.support.enums.action_enum import ActionEnum
from edkcore.support.properties.context_properties import ContextProperties


class MetaProperties(ContextProperties):
    def __init__(self):
        super().__init__()

    @property
    def acs(self):
        return self.get("acs", [])

    @acs.setter
    def acs(self, value):
        if len(self.acs) == 0:
            self._data["acs"] = [value]
        else:
            self._data["acs"].append(value)

    def property_type(self) -> ActionEnum: return ActionEnum.Meta

