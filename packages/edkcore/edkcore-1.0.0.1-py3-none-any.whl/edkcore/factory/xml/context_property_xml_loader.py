from lxml import etree

from edkcore.support.abstract.abc_xml_loader import AbcXMLLoader
from edkcore.support.context.data_info import DataInfo
from edkcore.support.persistents.persistent_device_info import PersistentDeviceInfo

from edkcore.support.properties.context_data_properties import ContextDataProperties


class ContextPropertyXMLLoader(AbcXMLLoader):
    def loader(self):
        for e in self.xml_define.getroot():
            return self.context_property(element=e)

    def context_property(self, element):
        properties = ContextDataProperties()
        self.set_pkg_info(properties, element)
        for e in element:
            # if e.tag.lower() == 'persistents':
            if self.equal(tag=e.tag, element_name='persistents'):
                for key, value in self.persistents(e).items():
                    properties.add_persistent(PersistentDeviceInfo(name=key,
                                                                   clazz=value.get("clazz"),
                                                                   configuration=value.get("configuration")))
            elif self.equal(tag=e.tag, element_name='datas'):
                for data_e in e:
                    data_info_dict = data_e.attrib
                    for ee in data_e:
                        data_info_dict["persistence_class"] = ""
                        data_info_dict["serialize_class"] = ""
                        data_info_dict["persistence_ref"] = ""
                        if self.equal(ee.tag, element_name="getter"):
                            data_info_dict["userInput"] = ee.attrib.get("userInput", "")
                            data_info_dict["getter_class"] = ee.attrib.get("class", "")
                        elif self.equal(ee.tag, element_name="persistent"):
                            data_info_dict["persistence_ref"] = ee.attrib.get("ref", "")
                            for eee in ee:
                                if self.equal(eee.tag, element_name="persistence"):
                                    data_info_dict["persistence_class"] = eee.attrib.get("class", "")
                                elif self.equal(eee.tag, element_name="serialize"):
                                    data_info_dict["serialize_class"] = eee.attrib.get("class", "")
                    properties.add_data(DataInfo(**data_info_dict))

        return properties

    def persistents(self, element) -> dict:
        p = {}
        if element.attrib.get("ref"):
            p.update(self.persistents(etree.parse(element.attrib.get("ref")).getroot()))
        for e in element:

            if self.equal(tag=e.tag, element_name='persistentdevice'):
                p[e.attrib.get("name")] = {"clazz": e.attrib.get("class"),
                                           "configuration": self.configurations(e)}
        return p

    def configurations(self, element):
        config = dict()
        for e in element:
            if self.equal(tag=e.tag, element_name='configurations'):
                for i in e:
                    if self.equal(tag=i.tag, element_name='configuration'):
                        config[i.attrib.get("name")] = i.text
        return config
