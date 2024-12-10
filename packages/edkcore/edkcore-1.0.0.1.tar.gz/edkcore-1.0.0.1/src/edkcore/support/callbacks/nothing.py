
from edkcore.support.abstract.abc_call_back import AbcCallBack


class Nothing(AbcCallBack):
    def call_back(self): ...
