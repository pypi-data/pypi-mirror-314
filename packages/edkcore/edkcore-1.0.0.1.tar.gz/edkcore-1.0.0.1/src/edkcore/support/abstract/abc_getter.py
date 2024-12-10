import abc

from edkcore.support.context.context_action_data import ContextActionData
from edkcore.support.context.data_info import DataInfo


class AbcGetter(abc.ABC):
    def __init__(self, context_action_data: ContextActionData, data_info: DataInfo):
        self.context_action_data = context_action_data
        self.data_info = data_info

    def get(self, *args, **kwargs):
        """
        通过 覆写 的 _getter 获取属性值
        特殊处理: 如果在 _getter 中直接返回 content.get(name), 则会获取列表中最后的值
        :param args:
        :type args:
        :param kwargs:
        :type kwargs:
        :return:
            如果值为空则返回一个默认值,
            以下为各个数据类型的默认值: int = 0, str = '', list = [], dict = {}
        :rtype:
        """
        result = self._getter(*args, **kwargs)
        if result is None:
            return eval(f'{self.data_info.dataType}()')
        if type(result) != eval(self.data_info.dataType):
            raise Exception(
                f'{self.data_info.name} Getter Type is Wrong \n Expect: {self.data_info.dataType}, Actual: {type(result)}')
        return result

    def user_input(self):
        """
        如果字段是由用户输入,该方法返回 XML 中的输入的值。
        而非中间过程中改变后的值
        :return:
        :rtype:
        """
        return self.data_info.userInput

    @abc.abstractmethod
    def _getter(self, *args, **kwargs):
        """
        在 覆写 _getter 方法的时候有以下两点注意
        1. 不要直接调用 context_data.get(name) 获取自身数据，会陷入无限循环调用
        2. 通过 context_data.content.get(name) 返回的是 list, 而不是单独的值
        :param args:
        :type args:
        :param kwargs:
        :type kwargs:
        :return:
        :rtype:
        """
        ...
