from edkcore.support.abstract.abc_persistent_device import AbcPersistentDevice
from edkcore.support.context.context_data import ContextData
from edkcore.support.persistents.persistent_device_info import PersistentDeviceInfo
from edkcore.tests.test_context_data.external.memory_persistent_device import MemoryPersistentDevice
from edkcore.tests.test_context_data.external.tinydb_persistent_device import TinydbPersistentDevice


class SimpleContextData(ContextData):
    def set(self, name, value):
        pass

    def __init__(self, context_action):
        super().__init__(context_action)
        self._props.add_persistent(PersistentDeviceInfo(name="Memory", clazz=MemoryPersistentDevice, configuration=dict()))
        self._props.add_persistent(
            PersistentDeviceInfo(name="TinyDB", clazz=TinydbPersistentDevice, configuration=dict(path="TinyDB.json")))

        self.content["login"] = ""
        self.content["pwd"] = ""

    def login(self, name, pwd):
        self.content["login"] = name
        self.content["pwd"] = pwd

    def clear(self):
        self.content["login"] = ""
        self.content["pwd"] = ""

    def persistence(self, persistent: AbcPersistentDevice):
        if persistent.name == "Memory":
            persistent.ins().update(self.content)
        elif persistent.name == "TinyDB":
            tdb = persistent.ins()
            table = tdb.table("SimpleContextData")
            table.insert(dict(pwd=self.content.get("pwd")))

    def _serialize(self, persistent: AbcPersistentDevice):
        if persistent.name == "Memory":
            self.content["login"] = persistent.ins()["login"]
        elif persistent.name == "TinyDB":
            tdb = persistent.ins()
            table = tdb.table("SimpleContextData")
            self.content["pwd"] = table.all()[-1].get("pwd")
