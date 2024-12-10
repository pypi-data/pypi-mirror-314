from edkcore.factory.context_data_factory import ContextDataFactory
from edkcore.factory.xml.context_property_xml_loader import ContextPropertyXMLLoader
from edkcore.support.abstract.abc_context_action import AbcContextAction
from edkcore.support.abstract.abc_properties import AbcProperties
from edkcore.support.context.context_data import ContextData
from edkcore.support.properties.meta_properties import MetaProperties
from edkcore.support.utils import class_loader


class MetaAction(AbcContextAction):
    def __init__(self, prop: AbcProperties = MetaProperties()):
        super().__init__(prop)

    def _context_data(self, properties) -> ContextData:
        if properties.context_data:
            if properties.context_data.endswith(".xml"):
                cpx = ContextPropertyXMLLoader(path=properties.context_data)
                context_property = cpx.loader()
                return ContextDataFactory.factory(context_action=self, context_property=context_property)
            return ContextDataFactory.factory(context_action=self, context_clazz=properties.context_data)

    def get_prop(self) -> MetaProperties:
        return self.prop
