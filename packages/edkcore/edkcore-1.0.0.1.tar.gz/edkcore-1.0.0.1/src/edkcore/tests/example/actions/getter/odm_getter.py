from edkcore.support.abstract.abc_getter import AbcGetter


class ODMGetter(AbcGetter):
    def _getter(self, *args, **kwargs):
        if self.context_action_data.content.get("ODM"):
            return self.context_action_data.content.get("ODM")
