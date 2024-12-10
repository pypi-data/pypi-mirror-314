import pymysql

from edkcore.support.abstract.abc_persistent_device import AbcPersistentDevice
from edkcore.support.context.context_data import ContextData
from edkcore.support.properties.context_data_properties import ContextDataProperties


class SimpleXMLContextData(ContextData):
    def set(self, name, value):
        pass

    def __init__(self, context_action, properties: ContextDataProperties):
        super().__init__(context_action, properties)
        
        self.content["login"] = ""
        self.content["pwd"] = ""
        self.content["token"] = ""

    def clear(self):
        self.content["login"] = ""
        self.content["pwd"] = ""
        self.content["token"] = ""

    def login(self, name, pwd):
        self.content["login"] = name
        self.content["pwd"] = pwd
        self.content["token"] = name+pwd

    def persistence(self, persistent: AbcPersistentDevice):
        if persistent.name == "MemoryDict":
            persistent.ins().update(self.content)
        elif persistent.name == "TinyDB":
            tdb = persistent.ins()
            table = tdb.table("SimpleContextData")
            table.insert(dict(pwd=self.content.get("pwd")))
        elif persistent.name == "MySQL":
            connection = persistent.ins()
            try:
                with connection.cursor() as cursor:
                    # 准备 SQL 插入语句
                    sql = "INSERT INTO `test` (`token`) VALUES (%s)"
                    val = (self.content["login"]+self.content["pwd"])  # 这里是你要插入的数据

                    # 执行 SQL 语句
                    cursor.execute(sql, val)

                # 提交事务
                connection.commit()


            except pymysql.Error as e:
                print("错误：", e)
                # 如果发生错误，可以选择回滚事务
                connection.rollback()

            finally:
                # 关闭连接
                connection.close()

    def _serialize(self, persistent: AbcPersistentDevice):
        if persistent.name == "MemoryDict":
            self.content["login"] = persistent.ins()["login"]
        elif persistent.name == "TinyDB":
            tdb = persistent.ins()
            table = tdb.table("SimpleContextData")
            self.content["pwd"] = table.all()[-1].get("pwd")
        elif persistent.name == "MySQL":
            connection = persistent.ins()
            try:
                with connection.cursor() as cursor:
                    # 准备 SQL 查询语句
                    sql = "SELECT token FROM `test` ORDER BY id desc LIMIT 1"

                    # 执行 SQL 查询
                    cursor.execute(sql)

                    # 获取所有记录列表
                    results = cursor.fetchall()
                    for row in results:
                        self.content["token"] = row[0]  # 打印每一行数据，row 是一个元组

            except pymysql.Error as e:
                print("错误：", e)

            finally:
                # 关闭连接
                connection.close()