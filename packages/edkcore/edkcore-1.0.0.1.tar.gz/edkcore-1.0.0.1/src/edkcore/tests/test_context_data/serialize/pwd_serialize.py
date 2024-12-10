from edkcore.support.abstract.abc_serialize import AbcSerialize


class PwdSerialize(AbcSerialize):
    def serializing(self) -> list:
        tdb = self.ins()
        table = tdb.table("SimpleContextData")
        return [int(record.get(self.data_info.name)) for record in table.all()]