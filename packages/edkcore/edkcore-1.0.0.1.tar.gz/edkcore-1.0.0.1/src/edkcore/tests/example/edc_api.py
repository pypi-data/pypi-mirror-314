import cjen
from eclinical import EdcLoginService, Environment


class EDCApi(EdcLoginService):
    def __init__(self, environment: Environment = Environment.loader(envir="CPC2017")):
        super().__init__(environment)

    @cjen.http.get_mapping(uri="edc/data-entry")
    def data_entry(self, resp=None, **kwargs): ...

    @cjen.http.post_mapping(uri="edc/subject/registration")
    def create_subject(self, data, resp=None, **kwargs): ...

    @cjen.http.get_mapping(uri="edc/subject/{subject_id}/visit/list")
    def visit_list(self, path_variable, resp=None, **kwargs): ...

    @cjen.http.get_mapping(uri="edc/subject-form/{subject_form_id}/detail?pageNo=1&pageSize=25")
    def subject_form_detail(self, path_variable, resp=None, **kwargs): ...

    @cjen.http.post_mapping(uri="edc/study-site/{site_id}/info?pageNo=1&pageSize=25")
    def study_site_info(self, path_variable, resp=None, **kwargs): ...

    @cjen.http.get_mapping(uri="edc/subject/{subject_id}/info?myTask=false")
    def subject_info_mytask(self, path_variable, resp=None, **kwargs): ...
