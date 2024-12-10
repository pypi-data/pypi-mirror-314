from edkcore.support.context.context_data import ContextData
from edkcore.support.persistents.persistent_device_connector import PersistentDeviceConnector


class ContextPersistent:

    @classmethod
    def persistent(cls, context_data: ContextData):
        for persistent in context_data.persistents:
            PersistentDeviceConnector.connect(persistent).commit(context_data)

    @classmethod
    def serialization(cls, context_data: ContextData):
        for persistent in context_data.persistents:
            context_data.serialization(PersistentDeviceConnector.connect(persistent))
        return context_data


