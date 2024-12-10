from edkcore.support.abstract.abc_serialize import AbcSerialize


class OdmSerialize(AbcSerialize):
    def serializing(self) -> list:
        return self.ins().get(self.data_info.name)