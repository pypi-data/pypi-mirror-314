from edkcore.factory.xml.meta_xml_loader import MetaXMlLoader

from edkcore.support.properties.scene_properties import SceneProperties


class SceneXMLLoader(MetaXMlLoader):
    def loader(self) -> SceneProperties:
        for e in self.xml_define.getroot():
            return self.scene(e)

    def scene(self, element):
        properties = SceneProperties()
        self.scene_info(properties, element)
        for e in element:

            if self.equal(e.tag, 'properties'):
                self.properties(properties, e)

            elif self.equal(e.tag, 'acs'):
                for ac in e:
                    if self.equal(ac.tag, 'metaaction'):
                        properties.acs = self.meta(ac, 0)
        return properties

    def scene_info(self, properties: SceneProperties, element):
        for key, value in element.attrib.items():
            if key.lower() == "name": properties.name = value


