from edkcore.support.meta_action import MetaAction


class MetaVariable(MetaAction):

    def _on_execute(self):
        self.context = {"Number": int(self.prop.get("Number"))}
