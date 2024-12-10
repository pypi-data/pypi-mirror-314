from edkcore.support.enums.action_enum import ActionEnum
from edkcore.support.properties.context_properties import ContextProperties
from edkcore.support.properties.meta_properties import MetaProperties


class SceneProperties(MetaProperties):
    def __init__(self):
        super().__init__()

    @property
    def name(self): return self.get("name", "")

    @name.setter
    def name(self, value):  self.set("name", value)

    def property_type(self) -> ActionEnum: return ActionEnum.Scene


