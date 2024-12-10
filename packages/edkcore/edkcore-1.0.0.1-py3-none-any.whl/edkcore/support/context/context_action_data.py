from edkcore.support.abstract.abc_persistent_device import AbcPersistentDevice
from edkcore.support.context.context_content import ContextContent
from edkcore.support.context.context_data import ContextData
from edkcore.support.properties.context_data_properties import ContextDataProperties
from edkcore.support.utils import class_loader
import json


class ContextActionData(ContextData):
    """
    ContextAction的上下文共享数据
    content 为内置存放的数据字典，根据 Data name来存放数据，存放的为 list
    set 方法并不是替换原有数据，而是增加一条数据记录

    """

    def __init__(self, context_action, properties: ContextDataProperties = ContextDataProperties()):
        super(ContextActionData, self).__init__(context_action, properties)
        self.content = ContextContent(self.datas_info)
        # self.content = {data.name: [] for data in self.datas_info}

    def persistence(self, persistent: AbcPersistentDevice):
        """
        存储值到存储设备
        :param persistent:
        :type persistent:
        :return:
        :rtype:
        """
        for data in self.datas_info:
            if data.persistence_ref == persistent.name:
                if self.content.need_persistent(data.name):
                    """
                        把满足关键字的所有值（列表）传递你给自定义的Persistence
                        由Persistence决定如何存储
                    """
                    class_loader(data.persistence_class)(self, persistent).persistence(data,
                                                                                       self.content.get(data.name),
                                                                                       self.content.get_history(
                                                                                           data.name))

    def _serialize(self, persistent: AbcPersistentDevice):
        for data_info in self.datas_info:
            if data_info.persistence_ref == persistent.name:
                class_loader(data_info.serialize_class)(self, data_info, persistent).serialize()

    def get(self, name, *args, **kwargs):
        """
        根据 Data name 获取属性值
        :param name:
        :type name:
        :param args:
        :type args:
        :param kwargs:
        :type kwargs:
        :return:
            如果 Data 没设置 class,则返回 userInput
            如果 Data 设置 class, 则返回 执行 class 的 get 方法
        :rtype:
        """
        for data_info in self.datas_info:
            if data_info.name == name:
                if data_info.getter_class:
                    return class_loader(data_info.getter_class)(self, data_info).get(*args, **kwargs)
                return data_info.userInput

    def default(self, name):
        for data in self.datas_info:
            if data.name == name:
                if data.dataType == 'int': return int(data.userInput)
                if data.dataType == 'str': return str(data.userInput)
                return json.loads(data.userInput)

    def set(self, name, value):
        if name not in [data.name for data in self.datas_info]:
            raise Exception(f'{name} is not in {[data.name for data in self.datas_info]}')
        for data in self.datas_info:
            if data.name == name:
                if eval(data.dataType) != type(value):
                    raise Exception(f'{name} Expect {data.dataType}, but {type(value)}')
        self.content.set(name, value)
