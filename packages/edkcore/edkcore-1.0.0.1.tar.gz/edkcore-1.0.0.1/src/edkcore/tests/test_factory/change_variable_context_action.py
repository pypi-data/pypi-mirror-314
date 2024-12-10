from edkcore.support.abstract.abc_context_action import AbcContextAction
from edkcore.support.context.context_data import ContextData
from edkcore.tests.test_factory.sum_context_data import SumContextData


class ChangeVariableContextAction(AbcContextAction):
    def _context_data(self, properties) -> ContextData:
        return SumContextData(self)

    def _on_execute(self):
        self.context = {"Number": int(self.prop.get("Number"))}
