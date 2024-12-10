from edkcore.support.enums.action_enum import ActionEnum
from edkcore.support.properties.context_properties import ContextProperties


class AssertProperties(ContextProperties):
    def __init__(self):
        super().__init__()

    @property
    def expects(self):
        return self.get("expects", [])

    @expects.setter
    def expects(self, value: dict):
        if not self.get("expects", []): self.set("expects", [value])
        else:
            self._data["expects"].append(value)

    def expect(self, name):
        """
        根据 Field 名 , 获取断言的期望值
        :param name:
        :type name:
        :return:
        :rtype:
        """
        for field in self.expects:
            if field.get("name") == name: return field.get("expect")
        raise Exception(f"NO expect {name}")

    def property_type(self) -> ActionEnum: return ActionEnum.Assert
