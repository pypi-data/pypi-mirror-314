from pathlib import Path

from edkcore.factory.xml.assert_xml_loader import AssertXMLLoader
from edkcore.factory.xml.meta_xml_loader import MetaXMlLoader
from edkcore.factory.xml.scene_xml_loader import SceneXMLLoader
from edkcore.support.enums.action_enum import ActionEnum


class XMLLoaderFactory:
    """
    读取　XML　文件，生成对应的　Properties　实例的工厂类
    """
    @classmethod
    def factory(cls, path: Path, action_enum: ActionEnum):
        """
        根据　文件路径 ,　类型生成　Properties　实例
        :param path:  文件路径
        :type path:
        :param action_enum: 文件的枚举类型
        :type action_enum:
        :return:
        :rtype:
        """
        if action_enum == ActionEnum.Meta:
            return MetaXMlLoader(path).loader()
        elif action_enum == ActionEnum.Scene:
            return SceneXMLLoader(path).loader()
        elif action_enum == ActionEnum.Assert:
            return AssertXMLLoader(path).loader()
