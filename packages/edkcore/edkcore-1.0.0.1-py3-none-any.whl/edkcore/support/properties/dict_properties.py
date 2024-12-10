from edkcore.support.abstract.abc_properties import AbcProperties


class DictProperties(AbcProperties):
    def __init__(self):
        self._data = dict()

    def get(self, name: str, default=None):
        return self._data.get(name, default)

    def set(self, name: str, value):
        self._data[name] = value
