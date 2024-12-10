from edkcore.support.meta_action import MetaAction
from edkcore.support.context.context_data import ContextData
from edkcore.tests.test_factory.sum_context_data import SumContextData


class MetaIncrement(MetaAction):
    def _context_data(self, properties) -> ContextData:
        return SumContextData(self)

    def _on_execute(self):
        self.context.add()
