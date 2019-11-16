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
        connection = pymysql.connect(self.__db_host, self.__db_admin, self.__db_password, self.__db, charset='utf8')
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

    # 根据phone, password查找
    def retrieve(self, user):
        retrieve_user = None

        sql = 'select * from user where phone = "%s" and password = "%s"' % (user.get_phone(), user.get_password())
        connection = pymysql.connect(self.__db_host, self.__db_admin, self.__db_password, self.__db, charset='utf8')
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

    # 根据user_id查找
    def get(self, user_id):
        retrieve_user = None

        sql = 'select * from user where user_id = %s' % (user_id)
        connection = pymysql.connect(self.__db_host, self.__db_admin, self.__db_password, self.__db, charset='utf8')
        cursor = connection.cursor()
        try:
            cursor.execute(sql)
            result = cursor.fetchone()
            if result is not None:
                retrieve_user = User()
                retrieve_user.set_user_id(result[0])
                retrieve_user.set_phone(result[1])
                retrieve_user.set_password(result[2])
                retrieve_user.set_nick_name(result[3])
                retrieve_user.set_avatar(result[4])
                retrieve_user.set_background_photo(result[5])
                retrieve_user.set_signature(result[6])
                retrieve_user.set_rank(result[7])
        except:
            traceback.print_exc()
        finally:
            connection.close()
            cursor.close()

        return retrieve_user

    # 更新
    def update(self, user):
        sql = 'update user set nick_name = "%s", avatar = "%s", background_photo = "%s"' \
              ', signature = "%s" where user_id = %s' % (user.get_nick_name(), user.get_avatar(), user.get_background_photo(),
                                                         user.get_signature(), user.get_user_id())
        connection = pymysql.connect(self.__db_host, self.__db_admin, self.__db_password, self.__db, charset='utf8')
        cursor = connection.cursor()
        try:
            cursor.execute(sql)
            connection.commit()
            result = {"StatusCode":0}
        except:
            traceback.print_exc()
            result = {"StatusCode":-2}
        finally:
            connection.close()
            cursor.close()

        return result

    def update_avatar(self, user):
        sql = 'update user set avatar = "%s" where user_id = %s' % (user.get_avatar(), user.get_user_id())
        connection = pymysql.connect(self.__db_host, self.__db_admin, self.__db_password, self.__db, charset='utf8')
        cursor = connection.cursor()
        try:
            cursor.execute(sql)
            connection.commit()
            result = {"StatusCode":0,
                      "Avatar": user.get_avatar()}
        except:
            traceback.print_exc()
            result = {"StatusCode":-2}
        finally:
            connection.close()
            cursor.close()

        return result

    # 更新背景
    def update_background_photo(self, user):
        sql = 'update user set background_photo = "%s" where user_id = %s' % (user.get_background_photo(), user.get_user_id())
        connection = pymysql.connect(self.__db_host, self.__db_admin, self.__db_password, self.__db, charset='utf8')
        cursor = connection.cursor()
        try:
            cursor.execute(sql)
            connection.commit()
            result = {"StatusCode":0,
                      "Homepage": user.get_background_photo()}
        except:
            traceback.print_exc()
            result = {"StatusCode":-2}
        finally:
            connection.close()
            cursor.close()

        return result