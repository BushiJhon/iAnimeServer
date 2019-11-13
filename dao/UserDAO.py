import traceback
import pymysql

from pojo.User import User


class UserDAO:
    __db_host = '127.0.0.1'
    __db_admin = 'root'
    __db_password = 'root'
    __db = 'iAnimeSQL'

    # 增加用户
    def add(self, user):
        sql = 'insert into user(user_id, phone, password) values( null, "%s", "%s" )' % (
            user.get_phone(), user.get_password())
        connection = pymysql.connect(self.__db_host, self.__db_admin, self.__db_password, self.__db)
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

    # 查找
    def retrieve(self, user):
        retrieve_user = None

        sql = 'select * from user where phone = "%s" and password = "%s"' % (user.get_phone(), user.get_password())
        connection = pymysql.connect(self.__db_host, self.__db_admin, self.__db_password, self.__db)
        cursor = connection.cursor()
        try:
            cursor.execute(sql)
            result = cursor.fetchone()
            if result is not None:
                retrieve_user = User()
                retrieve_user.set_user_id(result[0])
                retrieve_user.set_phone(result[1])
                retrieve_user.set_password(result[2])
        except:
            traceback.print_exc()
        finally:
            connection.close()
            cursor.close()

        return retrieve_user
