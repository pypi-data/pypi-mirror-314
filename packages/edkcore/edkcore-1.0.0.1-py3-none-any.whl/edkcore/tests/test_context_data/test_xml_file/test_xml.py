from edkcore.factory.xml.context_property_xml_loader import ContextPropertyXMLLoader
from edkcore.support.persistents.dict_persistent_device import DictPersistentDevice
from edkcore.tests.test_context_data.external.mysql_persistent_device import MySqlPersistentDevice
from edkcore.tests.test_context_data.external.tinydb_persistent_device import TinydbPersistentDevice


def test_context_data():
    cpx = ContextPropertyXMLLoader(path="context_data.xml")
    m = cpx.loader()
    assert m.clazz == 'edkcore.tests.test_context_data.simple_xml_context_data.SimpleXMLContextData'
    assert m.persistents[0].name == 'TinyDB'
    assert m.persistents[0].clazz == TinydbPersistentDevice
    assert m.persistents[0].configuration.get("path") == 'TinyDB.json'
    assert m.persistents[1].name == 'MySQL'
    assert m.persistents[1].clazz == MySqlPersistentDevice
    assert m.persistents[1].configuration.get("host") == 'automation-01.chengdudev.edetekapps.cn'
    assert m.persistents[1].configuration.get("user") == 'root'
    assert m.persistents[1].configuration.get("password") == '123456'
    assert m.persistents[1].configuration.get("database") == 'context_test'
    assert m.persistents[1].configuration.get("port") == '3307'

    assert m.persistents[2].name == 'MemoryDict'
    assert m.persistents[2].clazz == DictPersistentDevice


def test_context_data_ref():
    cpx = ContextPropertyXMLLoader(path="context_data_ref.xml")
    m = cpx.loader()
    assert m.clazz == 'edkcore.tests.test_context_data.simple_xml_context_data.SimpleXMLContextData'
    assert m.persistents[0].name == 'TinyDB11'
    assert m.persistents[0].clazz == TinydbPersistentDevice
    assert m.persistents[0].configuration.get("path") == 'TinyDB11.json'

    assert m.persistents[1].name == 'MySQL'
    assert m.persistents[1].clazz == MySqlPersistentDevice
    assert m.persistents[1].configuration.get("host") == 'automation-01.chengdudev.edetekapps.cn'
    assert m.persistents[1].configuration.get("user") == 'root'
    assert m.persistents[1].configuration.get("password") == '123456'
    assert m.persistents[1].configuration.get("database") == 'context_test'
    assert m.persistents[1].configuration.get("port") == '3307'

    assert m.persistents[2].name == 'MemoryDict'
    assert m.persistents[2].clazz == DictPersistentDevice
    assert m.persistents[3].name == 'TinyDB'
    assert m.persistents[3].clazz == TinydbPersistentDevice
    assert m.persistents[3].configuration.get("path") == 'TinyDB.json'
