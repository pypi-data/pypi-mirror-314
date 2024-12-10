from edkcore.factory.context_data_factory import ContextDataFactory
from edkcore.factory.xml.context_property_xml_loader import ContextPropertyXMLLoader
from edkcore.support.context.context_persistent import ContextPersistent

from edkcore.tests.test_context_data.simple_context_data import SimpleContextData
from edkcore.tests.test_context_data.simple_xml_context_data import SimpleXMLContextData


def test_context_data():
    sda = SimpleContextData(None)
    sda.login("cpc", "123456")
    ContextPersistent.persistent(sda)
    sda.clear()
    assert sda.get("login") == ""
    assert sda.get("pwd") == ""
    ContextPersistent.serialization(sda)
    assert sda.get("login") == "cpc"
    assert sda.get("pwd") == "123456"

def test_xml_context():
    cpx = ContextPropertyXMLLoader(path="simple_xml_context_data.xml")
    m = cpx.loader()
    sda = ContextDataFactory.factory(None, m, SimpleXMLContextData)
    sda.login("cpc", "123456")
    ContextPersistent.persistent(sda)
    sda.clear()

    assert m.datas_info[0].dataType == "str"
    assert m.datas_info[0].name == "siteCode"
    assert m.datas_info[0].inputBy == "User"
    assert m.datas_info[0].userInput == "sss"
    assert m.datas_info[0].getter_class == ""
    assert m.datas_info[0].persistence_class == ""
    assert m.datas_info[0].serialize_class == ""

    assert m.datas_info[1].dataType == "int"
    assert m.datas_info[1].name == "siteCode"
    assert m.datas_info[1].inputBy == "Sys"
    assert m.datas_info[1].userInput == ""
    assert m.datas_info[1].persistence_ref == "MySQL"
    assert m.datas_info[1].getter_class == "com.xxxx"
    assert m.datas_info[1].persistence_class == "ssssss"
    assert m.datas_info[1].serialize_class == "cccccccc"





    assert sda.get("login") == ""
    assert sda.get("pwd") == ""
    assert sda.get("token") == ""
    ContextPersistent.serialization(sda)
    assert sda.get("login") == "cpc"
    assert sda.get("pwd") == "123456"
    assert sda.get("token") == "cpc123456"



