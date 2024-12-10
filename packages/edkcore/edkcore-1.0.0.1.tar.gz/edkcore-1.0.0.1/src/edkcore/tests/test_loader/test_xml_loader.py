from pathlib import Path

from edkcore.factory.xml.assert_xml_loader import AssertXMLLoader
from edkcore.factory.xml.meta_xml_loader import MetaXMlLoader
from edkcore.factory.xml.scene_xml_loader import SceneXMLLoader
from edkcore.factory.xml_loader_factory import XMLLoaderFactory
from edkcore.support.enums.action_enum import ActionEnum


def test_meta_action_loader():
    r = XMLLoaderFactory.factory(Path("test_meta_action.xml"), ActionEnum.Meta)
    # r = m.loader()
    assert r.clazz == 'class1'
    assert r.context_data == 'contextData1'
    assert r.description == '进入指定的Site,根据系统生产的受试者名创建受试者'
    assert r.acs[0].clazz == 'class2'
    assert r.acs[0].description == '进入Study页面获取Site所有信息'
    assert r.acs[1].clazz == 'class3'
    assert r.acs[1].description == '根据指定的SiteCode获取系统生成的受试者名'

    assert r.acs[2].clazz == 'class4'
    assert r.acs[2].description == '根据系统自动生成的受试者名,创建受试者'
    assert r.acs[2].acs[0].clazz == 'Y1'

    assert r.acs[2].acs[0].description == '根据指定的SiteCode获取系统生成的受试者名'

    assert r.acs[2].acs[1].clazz == 'Y2'
    assert r.acs[2].acs[1].description == '根据指定的SiteCode获取系统生成的受试者名'

    assert r.acs[2].acs[2].clazz == 'Y3'

    assert r.acs[3].clazz == 'Aclass5'
    assert r.acs[3].description == '测试AssertAction'
    assert r.acs[3].expects[0].get("name") == '字段名1'
    assert r.acs[3].expects[0].get("description") == '描述1'
    assert r.acs[3].expects[0].get("expect") == '期望值1'
    assert r.acs[3].expects[1].get("name") == '字段名2'
    assert r.acs[3].expects[1].get("description") == '描述2'
    assert r.acs[3].expects[1].get("expect") == '期望值2'
    assert r.acs[3].expects[2].get("name") == '字段名3'
    assert r.acs[3].expects[2].get("description") == '描述3'
    assert r.acs[3].expects[2].get("expect") == '期望值3'
    assert r.acs[3].expects[3].get("name") == '字段名4'
    assert r.acs[3].expects[3].get("description") == '描述4'
    assert r.acs[3].expects[3].get("expect") == '期望值4'
    assert r.acs[3].expects[4].get("name") == '字段名5'
    assert r.acs[3].expects[4].get("description") == '描述5'
    assert r.acs[3].expects[4].get("expect") == '期望值5'
    assert r.acs[4].clazz == 'Cclass1'


def test_assert_xml_loader():
    r = XMLLoaderFactory.factory(Path("test_assert_action.xml"), ActionEnum.Assert)
    assert r.description == "测试AssertAction"
    assert len(r.expects) == 5

    assert r.expects[0].get("name") == '字段名1'
    assert r.expects[0].get("description") == '描述1'
    assert r.expects[0].get("expect") == '期望值1'
    assert r.expects[1].get("name") == '字段名2'
    assert r.expects[1].get("description") == '描述2'
    assert r.expects[1].get("expect") == '期望值2'
    assert r.expects[2].get("name") == '字段名3'
    assert r.expects[2].get("description") == '描述3'
    assert r.expects[2].get("expect") == '期望值3'
    assert r.expects[3].get("name") == '字段名4'
    assert r.expects[3].get("description") == '描述4'
    assert r.expects[3].get("expect") == '期望值4'
    assert r.expects[4].get("name") == '字段名5'
    assert r.expects[4].get("description") == '描述5'
    assert r.expects[4].get("expect") == '期望值5'


def test_scene_action():
    r = XMLLoaderFactory.factory(Path("test_scene.xml"), ActionEnum.Scene)
    assert r.name == 'TestScene'
    assert r.acs[0].context_data == "cd1"
    assert r.acs[1].context_data == "cd2"
    assert r.acs[2].context_data == "cd3"

# if __name__ == '__main__':
#     m = MetaXMlLoader(Path("test_meta_action.xml"))
#     r = m.loader()
#     print(r)
