from edkcore.support.abstract.abc_context_action import AbcContextAction
from edkcore.support.context.context_action_data import ContextActionData
from edkcore.support.context.context_data import ContextData
from edkcore.support.context.context_persistent import ContextPersistent
from edkcore.tests.example.actions.getter.odm_id_getter import OdmIdGetter
from edkcore.tests.example.edc_api import EDCApi


class CreateSubjectAction(AbcContextAction):
    def _context_data(self, properties) -> ContextData:
        return ContextActionData(self)

    def _on_before(self):
        # super(CreateSubjectAction, self)._on_before()
        self.api = EDCApi()

    def _on_execute(self):
        resp = self.api.create_subject(data={
            "name": self.context.get("subjectName"),
            "studySiteId": self.context.get("odmId", OdmIdGetter.Site, [self.context.get("SiteCode")]),
            "enrollPhase": False,
            "visitDate": 1717468332000,
            "propertyValueMap": {}
        })
        print(resp)

