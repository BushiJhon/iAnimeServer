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
        sql = 'insert into user(user_id, phone, password) values( null, %s, "%s" )' % (
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
        sql = 'select * from user where phone = %s and password = "%s"' % (user.get_phone(), user.get_password())
        connection = pymysql.connect(self.__db_host, self.__db_admin, self.__db_password, self.__db)
        cursor = connection.cursor()
        try:
            cursor.execute(sql)
            retrieve_user = cursor.fetchone()
        except:
            traceback.print_exc()
        finally:
            connection.close()
            cursor.close()
        print(retrieve_user)
        return


user = User()
# user.set_phone(17802002999)
# user.set_password('John')
# user_dao = UserDAO()
# user_dao.retrieve(user)
