from edkcore.support.context.data_info import DataInfo


class ContextContent:
    def __init__(self, datas_info: list[DataInfo]):

        self._content = {data.name: self.init_default(data) for data in datas_info}
        self._history_changes = {data.name: [] for data in datas_info}
        self._changes_flag = {data.name: [] for data in datas_info}

    def init_default(self, data_info: DataInfo):
        """
        给定义的的 Data 赋予初始值
        目前只有基本类型才有默认值
        :param data_info:
        :type data_info:
        :return:
        :rtype:
        """
        if data_info.dataType == 'str':
            return ""
        elif data_info.dataType == 'int':
            return 0
        elif data_info.dataType == "dict":
            return {}
        elif data_info.dataType == "list":
            return []
        return None

    def get(self, name):
        return self._content.get(name)

    def get_history(self, name) -> list:
        return self._history_changes.get(name)

    def set(self, name, value):
        self._content[name] = value

        if type(value) in [int, str, float]:
            self._history_changes.get(name).append(value)
        else:
            self._history_changes.get(name).append(value.copy())
        self._changes_flag.get(name).append(1)

    def need_persistent(self, name):
        if not self._content.get(name): return False
        if not self._changes_flag.get(name): return False
        return True

    def persistent(self, name):
        self._changes_flag.get(name).clear()
