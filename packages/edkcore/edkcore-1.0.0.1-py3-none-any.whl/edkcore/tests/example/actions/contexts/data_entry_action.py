from edkcore.support.abstract.abc_context_action import AbcContextAction
from edkcore.support.context.context_action_data import ContextActionData
from edkcore.support.context.context_data import ContextData
from edkcore.tests.example.edc_api import EDCApi


class DataEntryAction(AbcContextAction):

    def _context_data(self, properties) -> ContextData:
        return ContextActionData(self)

    def _on_before(self):
        self.api = EDCApi()

    def _on_execute(self):
        resp = self.api.data_entry()
        for dto in resp.get("payload").get("studySiteInfoDtos"):
            if dto.get("code") == self.context.get("SiteCode"):
                odm = self.context.get("ODM")
                odm[self.context.get("SiteCode")] = dto.get("studySiteId")
                self.context.set("ODM", odm)
