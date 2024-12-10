import pymysql

from edkcore.support.abstract.abc_persistence import AbcPersistence


class TokenPersistence(AbcPersistence):
    def persistence(self, data_info, cur_data, his_data: list):
        connection = self.ins()
        try:
            with connection.cursor() as cursor:
                # 准备 SQL 插入语句
                sql = "INSERT INTO `test` (`token`) VALUES (%s)"
                val = (his_data)  # 这里是你要插入的数据

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
