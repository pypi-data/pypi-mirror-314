from edkcore.support.abstract.abc_getter import AbcGetter


class PwdGetter(AbcGetter):
    def _getter(self, *args, **kwargs):
        return self.context_action_data.content.get("pwd")
