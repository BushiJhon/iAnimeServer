import traceback

import pymysql

from dao.DatabaseConfig import *


class FollowDAO:
    __db_host = host
    __db_admin = admin
    __db_password = password
    __db = database
    __port = port
    __charset = charset

    # 添加
    def add(self, user_id, follower_id):
        sql = 'insert into follow values(%s, %s)' % (user_id, follower_id)
        connection = pymysql.connect(host=self.__db_host, user=self.__db_admin, password=self.__db_password,
                                     database=self.__db, port=self.__port, charset=self.__charset)
        cursor = connection.cursor()
        try:
            cursor.execute(sql)
            connection.commit()
        except:
            traceback.print_exc()
            connection.rollback()
        finally:
            connection.close()
            cursor.close()
        return

    # 删除
    def delete(self, user_id, follower_id):
        sql = 'delete from follow where user_id = %s and follower_id = %s' % (user_id, follower_id)
        connection = pymysql.connect(host=self.__db_host, user=self.__db_admin, password=self.__db_password,
                                     database=self.__db, port=self.__port, charset=self.__charset)
        cursor = connection.cursor()
        try:
            cursor.execute(sql)
            connection.commit()
        except:
            traceback.print_exc()
            connection.rollback()
        finally:
            connection.close()
            cursor.close()
        return
