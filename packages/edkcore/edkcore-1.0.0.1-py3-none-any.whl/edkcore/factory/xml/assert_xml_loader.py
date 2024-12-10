from edkcore.support.abstract.abc_xml_loader import AbcXMLLoader
from edkcore.support.properties.assert_properties import AssertProperties


class AssertXMLLoader(AbcXMLLoader):
    def loader(self):
        for e in self.xml_define.getroot():
            return self.assert_action(e)

    def assert_action(self, element):
        properties = AssertProperties()
        self.set_pkg_info(properties, element)

        for e in element:
            if self.equal(e.tag, 'properties'):
                self.properties(properties, e)
            elif self.equal(e.tag, 'expects'):
                for ec in e:
                    if self.equal(ec.tag, 'field'):
                        field = dict()
                        for key, value in ec.attrib.items():
                            field[key.lower()] = value
                        properties.expects = field
        return properties
