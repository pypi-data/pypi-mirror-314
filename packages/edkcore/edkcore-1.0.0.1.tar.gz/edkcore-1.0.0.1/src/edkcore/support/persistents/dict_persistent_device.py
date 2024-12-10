from edkcore.support.abstract.abc_persistent_device import AbcPersistentDevice


class DictPersistentDevice(AbcPersistentDevice):
    def _on_configuration(self, configuration: dict):
        pass

    cache_persistent = dict()

    def ins(self):
        return DictPersistentDevice.cache_persistent
