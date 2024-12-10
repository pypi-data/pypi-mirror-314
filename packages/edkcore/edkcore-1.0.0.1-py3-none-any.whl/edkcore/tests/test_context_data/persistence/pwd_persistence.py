from edkcore.support.abstract.abc_persistence import AbcPersistence


class PwdPersistence(AbcPersistence):
    def persistence(self, data_info, cur_data, his_data: list):
        tdb = self.ins()
        table = tdb.table("SimpleContextData")
        table.insert({data_info.name : his_data})