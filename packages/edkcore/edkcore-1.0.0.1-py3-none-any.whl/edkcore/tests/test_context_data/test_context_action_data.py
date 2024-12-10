from edkcore.factory.context_data_factory import ContextDataFactory
from edkcore.factory.xml.context_property_xml_loader import ContextPropertyXMLLoader
from edkcore.support.context.context_persistent import ContextPersistent


def test_context_action_data():
    cpx = ContextPropertyXMLLoader(path="simple_context_action_data.xml").loader()
    context_data = ContextDataFactory.factory(None, cpx)
    assert context_data.get("login") == 'sss'

    context_data.set("pwd", 1234)
    assert context_data.get("pwd") == 1234
    context_data.set("token", context_data.get("login") + str(context_data.get("pwd")))
    ContextPersistent.persistent(context_data)
    new_context_data = ContextDataFactory.factory(None, cpx)
    ContextPersistent.serialization(new_context_data)
    assert new_context_data.get("login") == 'sss'
    assert new_context_data.get("pwd") == 1234
    assert new_context_data.get("token") == 'sss1234'


