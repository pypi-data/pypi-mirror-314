from edkcore.factory.xml.assert_xml_loader import AssertXMLLoader
from edkcore.support.properties.context_properties import ContextProperties
from edkcore.support.properties.meta_properties import MetaProperties


class MetaXMlLoader(AssertXMLLoader):

    def loader(self) -> MetaProperties:
        for e in self.xml_define.getroot():
            return self.meta(element=e, level=0)

    def meta(self, element, level: int = 0) -> MetaProperties:
        properties = MetaProperties()
        if level == 0:
            if "contextdata" not in [e.lower() for e in element.attrib.keys()]:
                raise Exception("根节点的MetaAction需设置 ContextData")
        self.set_pkg_info(properties, element)

        for e in element:

            if self.equal(e.tag, 'properties'):
                self.properties(properties, e)
            elif self.equal(e.tag, 'acs'):
                for ac in e:

                    if self.equal(ac.tag, 'metaaction'):
                        properties.acs = self.meta(ac, level + 1)

                    elif self.equal(ac.tag, 'assertaction'):
                        properties.acs = self.assert_action(ac)

                    elif self.equal(ac.tag, 'contextaction'):
                        properties.acs = self.context(ac)
        return properties

    def context(self, element) -> ContextProperties:
        properties = ContextProperties()
        self.set_pkg_info(properties, element)

        for e in element:

            if self.equal(e.tag, 'properties'):
                self.properties(properties, e)
        return properties






