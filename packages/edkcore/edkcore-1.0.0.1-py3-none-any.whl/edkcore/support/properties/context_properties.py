from edkcore.support.enums.action_enum import ActionEnum
from edkcore.support.properties.dict_properties import DictProperties


class ContextProperties(DictProperties):
    @property
    def description(self): return self.get("description", "")

    @description.setter
    def description(self, value): self.set("description", value)

    @property
    def context_data(self): return self.get("contextData", "")

    @context_data.setter
    def context_data(self, value): self.set("contextData", value)

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

    def property_type(self) -> ActionEnum: return ActionEnum.Context
