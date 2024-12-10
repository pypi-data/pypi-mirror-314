import pathlib

from edkcore.factory.xml_loader_factory import XMLLoaderFactory
from edkcore.support.meta_action import MetaAction
from edkcore.support.enums.action_enum import ActionEnum


class XMLMetaAction(MetaAction):
    def _on_init(self):
        from edkcore.factory.context_action_factory import ContextActionFactory
        for ac in self.prop.get('acs'):
            if ac.path:
                ac_prop = XMLLoaderFactory.factory(path=pathlib.Path(ac.path), action_enum=ac.property_type())
                self.append(ContextActionFactory.factory(ac_prop))
            else: self.append(ContextActionFactory.factory(ac))
