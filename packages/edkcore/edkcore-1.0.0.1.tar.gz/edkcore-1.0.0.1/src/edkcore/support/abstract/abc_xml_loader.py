import abc

from lxml import etree

from edkcore.support.properties.context_properties import ContextProperties


class AbcXMLLoader(abc.ABC):
    def __init__(self, path):
        self.xml_define = etree.parse(path)

    @property
    def namespace(self):
        return "{http://www.edkcore.org/XMLSchema}"

    def equal(self, tag: str, element_name: str) -> bool:
        return tag.replace(self.namespace, "").lower() == element_name

    @abc.abstractmethod
    def loader(self):
        """
        抽象方法，具体实现放在子类
        主要作用，返回读取的　XML文件　生成的　Properties 对象
        :return:
        :rtype:
        """
        ...

    def set_pkg_info(self, properties: ContextProperties, element):
        for key, value in element.attrib.items():
            if key.lower() == "class":
                if properties.path is not None:
                    raise Exception("XML class and path can not exist at same time")
                properties.clazz = value
            elif key.lower() == "contextdata":
                properties.context_data = value
            elif key.lower() == "path":
                if properties.clazz is not None:
                    raise Exception("XML class and path can not exist at same time")
                properties.path = value

    def properties(self, properties: ContextProperties, element):
        for e in element:
            if e.attrib.get("name").lower() == "description":
                properties.set('description', e.text)
            else:
                properties.set(e.attrib.get("name"), e.text)
