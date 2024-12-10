import pymysql

from edkcore.support.abstract.abc_persistent_device import AbcPersistentDevice


class MySqlPersistentDevice(AbcPersistentDevice):
    def _on_configuration(self, configuration: dict):
        self._configuration = configuration
        self._configuration["port"] = int(self._configuration["port"])

    def ins(self):
        return pymysql.connect(**self._configuration)
