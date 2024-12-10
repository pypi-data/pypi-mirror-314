import pathlib

from edkcore.support.abstract.abc_persistent_device import AbcPersistentDevice

from tinydb import TinyDB


class TinydbPersistentDevice(AbcPersistentDevice):
    def _on_configuration(self, configuration):
        self._path = pathlib.Path(configuration.get("path"))

    def ins(self):
        if not self._path.exists():
            self._path.parent.mkdir(parents=True, exist_ok=True)
        return TinyDB(self._path)
