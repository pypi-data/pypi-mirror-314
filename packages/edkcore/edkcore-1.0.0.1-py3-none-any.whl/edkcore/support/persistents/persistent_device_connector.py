from edkcore.support.abstract.abc_persistent_device import AbcPersistentDevice
from edkcore.support.persistents.persistent_device_info import PersistentDeviceInfo
from edkcore.support.utils import new_class


class PersistentDeviceConnector:

    @classmethod
    def connect(cls, device_info: PersistentDeviceInfo) -> AbcPersistentDevice:
        connection = new_class(device_info.clazz, device_info)
        return connection
