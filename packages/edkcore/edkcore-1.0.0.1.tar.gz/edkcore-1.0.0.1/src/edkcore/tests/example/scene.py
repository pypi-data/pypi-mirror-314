import pathlib

from edkcore.factory.context_action_factory import ContextActionFactory
from edkcore.factory.xml_loader_factory import XMLLoaderFactory
from edkcore.support.enums.action_enum import ActionEnum

if __name__ == '__main__':
    # m = XMLLoaderFactory.factory(path=pathlib.Path("actions/metas/create_subject_meta.xml"), action_enum=ActionEnum.Meta)
    m = XMLLoaderFactory.factory(path=pathlib.Path("actions/metas/data_entry_meta.xml"), action_enum=ActionEnum.Meta)
    a = ContextActionFactory.factory(m)
    a.execute()
    # print(a.context.get("ODM"))