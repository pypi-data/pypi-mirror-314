from edkcore.support.abstract.abc_persistent_device import AbcPersistentDevice


class MemoryPersistentDevice(AbcPersistentDevice):
    def _on_configuration(self, configuration):
        pass

    cache_persistent = dict()

    def ins(self):
        return MemoryPersistentDevice.cache_persistent
