from edkcore.support.abstract.abc_context_action import AbcContextAction
from edkcore.support.context.context_action_data import ContextActionData
from edkcore.support.context.context_data import ContextData
from edkcore.tests.example.actions.getter.odm_id_getter import OdmIdGetter
from edkcore.tests.example.edc_api import EDCApi


class EnterCrfAction(AbcContextAction):

    def _context_data(self, properties) -> ContextData:
        return ContextActionData(self)

    def _on_before(self):
        # super(CreateSubjectAction, self)._on_before()
        self.api = EDCApi()

    # def set_odm(self, key, value):
    #     odm = self.context.get("ODM")
    #     odm[key] = value
    #     self.context.set("ODM", odm)

    def _on_execute(self):
        self.get_site() or self.get_subject() or self.get_visit_form_ig()
        print(self.context.get("ODM"))

    def get_site(self):
        if self.context.get("SiteCode"):
            resp = self.api.data_entry()
            for dto in resp.get("payload").get("studySiteInfoDtos"):
                if dto.get("code") == self.context.get("SiteCode"):
                    odm = self.context.get("ODM")
                    odm[self.context.get("SiteCode")] = dict(id=dto.get("studySiteId"))
                    self.context.set("ODM", odm)

                    return False
        return True

    def get_subject(self):
        if self.context.get("SubjectName"):
            resp = self.api.study_site_info(path_variable=dict(
                site_id=self.context.get("odmId", OdmIdGetter.Site, [self.context.get("SiteCode")])))
            for dto in resp.get("payload").get("subjectInfoDtos").get("list"):
                if dto.get("subjectName") == self.context.get("SubjectName"):
                    odm = self.context.get("ODM")
                    odm[self.context.get("SiteCode")][self.context.get("SubjectName")] = dict(id=dto.get("id"))
                    return False
        return True

    def get_visit_form_ig(self):
        if self.context.get("Visit"):
            resp = self.api.subject_info_mytask(
                path_variable=dict(
                    subject_id=self.context.get("odmId", OdmIdGetter.Subject,
                                                [self.context.get("SiteCode"),
                                                 self.context.get("Subject")])))
            for dto in resp.get("payload").get("subjectVisitTaskDtoList"):
                if dto.get("name") == self.context.get("Visit"):
                    odm = self.context.get("ODM")
                    odm[self.context.get("SiteCode")][self.context.get("SubjectName")][
                        self.context.get("Visit")] = dict(id=dto.get("id"))

                    return self.get_form(dto.get("subjectFormTaskDtoList"))
        return True

    def get_form(self, form_list):
        if self.context.get("Form"):
            for form in form_list:
                if form.get("name") == self.context.get("Form"):
                    odm = self.context.get("ODM")
                    odm[self.context.get("SiteCode")][self.context.get("SubjectName")][
                        self.context.get("Visit")][self.context.get("Form")] = dict(id=form.get("id"))

                    return self.get_ig(form.get("subjectIgTaskDtoList"))
        return True

    def get_ig(self, ig_list):
        if self.context.get("Ig"):
            for ig in ig_list:
                if ig.get("name") == self.context.get("Ig"):
                    odm = self.context.get("ODM")
                    odm[self.context.get("SiteCode")][self.context.get("SubjectName")][
                        self.context.get("Visit")][self.context.get("Form")][self.context.get("Ig")] = dict(
                        id=ig.get("id"))

                    return False
        return True
