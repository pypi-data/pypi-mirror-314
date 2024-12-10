from edkcore.support.abstract.abc_persistence import AbcPersistence


class OdmPersistence(AbcPersistence):
    def persistence(self, data_info, cur_data, his_data: list):
        self.ins().update({data_info.name: his_data})

