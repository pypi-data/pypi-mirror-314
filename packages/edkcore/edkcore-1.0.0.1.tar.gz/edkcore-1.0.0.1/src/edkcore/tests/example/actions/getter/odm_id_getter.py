import site

from edkcore.support.abstract.abc_getter import AbcGetter


class OdmIdGetter(AbcGetter):
    Site = "Site"
    Subject = "Subject"
    Visit = "Visit"
    Form = "Form"
    Ig = "Ig"
    Item = "Item"

    def _getter(self, odm_type: str, odm_path: list[str]):
        if odm_type == self.Site:
            site = odm_path[0]
            return self.context_action_data.get("ODM").get(site).get("id")
        elif odm_type == self.Subject:
            site, subject = odm_path
            return self.context_action_data.get("ODM").get(site).get(subject).get("id")
        elif odm_type == self.Visit:
            site, subject, visit = odm_path
            return self.context_action_data.get("ODM").get(site).get(subject).get(visit).get("id")
        elif odm_type == self.Form:
            site, subject, visit = odm_path
            return self.context_action_data.get("ODM").get(site).get(subject).get(visit).get("id")
        elif odm_type == self.Ig:
            site, subject, visit, ig = odm_path
            return self.context_action_data.get("ODM").get(site).get(subject).get(visit).get(ig).get("id")








