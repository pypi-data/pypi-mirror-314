import pymysql

from edkcore.support.abstract.abc_serialize import AbcSerialize


class TokenSerialize(AbcSerialize):
    def serializing(self) -> list:
        connection = self.ins()
        try:
            with connection.cursor() as cursor:
                # 准备 SQL 查询语句
                sql = "SELECT token FROM `test`"

                # 执行 SQL 查询
                cursor.execute(sql)

                # 获取所有记录列表
                results = cursor.fetchall()
                return [row[0] for row in results]
        except pymysql.Error as e:
            print("错误：", e)

        finally:
            # 关闭连接
            connection.close()
