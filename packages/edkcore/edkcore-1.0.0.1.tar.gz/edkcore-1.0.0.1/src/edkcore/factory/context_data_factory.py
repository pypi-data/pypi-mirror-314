from edkcore.support.properties.context_data_properties import ContextDataProperties

from edkcore.support.utils import new_class


class ContextDataFactory:
    @classmethod
    def factory(cls, context_action, context_property=ContextDataProperties(), context_clazz=None):
        """
        创建 ContextData 的实例工厂方法
        :param context_action: ContextData所属的 ContextAction
        :type context_action:
        :param context_property: context_property 属性
        :type context_property:
        :param context_clazz: context_clazz ContextData的实现类,当是通过XML 的方式创建的时候,该参数可不指定
        :type context_clazz:
        :return:
        :rtype:
        """

        __clazz = context_clazz if context_clazz is not None else context_property.clazz
        return new_class(__clazz, context_action, context_property)


