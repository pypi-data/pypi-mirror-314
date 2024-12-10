
from edkcore.support.enums.action_enum import ActionEnum
from edkcore.support.properties.context_properties import ContextProperties
from edkcore.support.utils import new_class
from edkcore.support.xml_meta_action import XMLMetaAction
from edkcore.support.xml_scene_action import XMLSceneAction


class ContextActionFactory:
    """
    读取　Properties　文件，生成　Action　实例的工厂类
    """
    @classmethod
    def factory(cls, properties: ContextProperties):
        """
        根据　属性对象 ,　类型生成　Action　实例
        :param properties: 属性对象
        :type properties:
        :return:
        :rtype:
        """
        if properties.clazz:
            # return class_loader(properties.clazz)(properties)
            return new_class(properties.clazz, properties)
        else:
            if properties.property_type() == ActionEnum.Meta:
                return XMLMetaAction(properties)
            elif properties.property_type() == ActionEnum.Scene:
                return XMLSceneAction(properties)
