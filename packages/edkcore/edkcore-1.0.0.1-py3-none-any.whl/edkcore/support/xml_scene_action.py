from edkcore.support.abstract.abc_context_action import AbcContextAction
from edkcore.support.context.context_data import ContextData
from edkcore.support.properties.scene_properties import SceneProperties
from edkcore.support.xml_meta_action import XMLMetaAction


class XMLSceneAction(XMLMetaAction):
    def __init__(self, prop: SceneProperties):
        super().__init__(prop)

    def get_prop(self) -> SceneProperties: return self.prop

    def _context_data(self, properties) -> ContextData: pass
