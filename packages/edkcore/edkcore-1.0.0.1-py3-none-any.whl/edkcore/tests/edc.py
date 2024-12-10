from eclinical import EdcLoginService, Environment
import cjen


class EDC(EdcLoginService):
    def __init__(self, environment: Environment = None):
        super().__init__(environment)

    @cjen.http.post_mapping(uri="edc/study-site/{siteID}/info?pageNo=1&pageSize=25")
    def study_site(self, path_variable: dict, data, resp=None, **kwargs): ...

    @cjen.http.post_mapping(uri="edc/subject-name/{siteID}")
    def subject_name(self, path_variable: dict, resp=None, **kwargs): ...

    @cjen.http.post_mapping(uri="edc/subject/registration")
    def registration(self, data, resp=None, **kwargs): ...

    @cjen.http.get_mapping(uri="edc/data-entry")
    def data_entry(self, resp=None, **kwargs): ...

