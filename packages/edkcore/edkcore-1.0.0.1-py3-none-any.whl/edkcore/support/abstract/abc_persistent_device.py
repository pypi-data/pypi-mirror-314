import abc

from edkcore.support.persistents.persistent_device_info import PersistentDeviceInfo


class AbcPersistentDevice(abc.ABC):

    def __init__(self, device_info: PersistentDeviceInfo):
        self._name = device_info.name
        self._on_configuration(device_info.configuration)

    @property
    def name(self): return self._name

    @name.setter
    def name(self, value): self._name = value

    @abc.abstractmethod
    def _on_configuration(self, configuration: dict):
        """
        子类实现 配置 连接存储实例的参数
        比如 mysql 就是配置 host, user, password, ...

        :param configuration: PersistentInfo 存储设配的配置
        :type configuration:
        :return:
        :rtype:
        """
        ...

    @abc.abstractmethod
    def ins(self):
        """
        获取 持久化存储的实例
        假如是 pymysql 返回 pymysql 的实例
        假如是 其它存储 返回 其它存储 的实例
        *args, **kwargs 连接信息
        :return:
        :rtype:
        """
        ...

    def commit(self, context_data):
        """
        提交数据，保存在持久化存储中
        :param context_data:
        :type context_data:
        :return:
        :rtype:
        """
        context_data.persistence(self)
