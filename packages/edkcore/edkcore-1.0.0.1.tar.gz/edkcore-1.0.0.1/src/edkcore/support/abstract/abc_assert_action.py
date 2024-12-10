import abc

from edkcore.support.abstract.abc_context_action import AbcContextAction
from edkcore.support.context.context_data import ContextData
from edkcore.support.properties.assert_properties import AssertProperties
from edkcore.support.utils import class_loader


class AbcAssertAction(AbcContextAction):
    def _context_data(self, properties) -> ContextData:
        if properties.context_data:
            return class_loader(properties.context_data)(self)

    def get_prop(self) -> AssertProperties:
        return self.prop

    def _on_execute(self):
        self.assert_expect()

    @abc.abstractmethod
    def assert_expect(self): ...

