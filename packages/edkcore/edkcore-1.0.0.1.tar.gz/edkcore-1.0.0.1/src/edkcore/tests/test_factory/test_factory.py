from pathlib import Path

from edkcore.factory.context_action_factory import ContextActionFactory

from edkcore.factory.xml.meta_xml_loader import MetaXMlLoader
from edkcore.factory.xml.scene_xml_loader import SceneXMLLoader



def test_one():
    meta_properties = MetaXMlLoader(Path('MetaVariable.xml')).loader()
    meta = ContextActionFactory.factory(meta_properties)
    meta.execute()
    assert meta.context.get(meta.uid)["Number"] == 2


def test_many():
    meta_properties = MetaXMlLoader(Path('AddMetas.xml')).loader()
    meta = ContextActionFactory.factory(meta_properties)
    meta.execute()
    # assert meta.context.get("count") == 4


def test_scene():
    scene_properties = SceneXMLLoader(Path("scene_sum.xml")).loader()
    scene = ContextActionFactory.factory(scene_properties)
    scene.execute()


