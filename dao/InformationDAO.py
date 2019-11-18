import traceback

import pymysql

from dao.DatabaseConfig import *


class InformationDAO:
    __db_host = host
    __db_admin = admin
    __db_password = password
    __db = database
    __port = port
    __charset = charset

    # 查找
    def retrieve(self, information):

        sql = 'select * from information where user_id = %s' % (information.get_user_id())
        connection = pymysql.connect(host=self.__db_host, user=self.__db_admin, password=self.__db_password,
                                     database=self.__db, port=self.__port, charset=self.__charset)
        cursor = connection.cursor()
        try:
            cursor.execute(sql)
            result = cursor.fetchone()
            if result is not None:
                information.set_nick_name(result[1])
                information.set_avatar(result[2])
                information.set_background_photo(result[3])
                information.set_signature(result[4])
                information.set_rank(result[5])
                sql = 'select count(*) from follow where user_id = %s;' % information.get_user_id()
                cursor.execute(sql)
                result = cursor.fetchone()
                information.set_following(result[0])
                sql = 'select count(*) from follow where follower_id = %s;' % information.get_user_id()
                cursor.execute(sql)
                result = cursor.fetchone()
                information.set_follower(result[0])
            else:
                information = None
        except:
            traceback.print_exc()
        finally:
            connection.close()
            cursor.close()

        return information

    # 更新
    def update(self, information):
        sql = 'update information set nick_name = "%s", avatar = "%s", background_photo = "%s"' \
              ', signature = "%s" where user_id = %s' % (
                  information.get_nick_name(), information.get_avatar(), information.get_background_photo(),
                  information.get_signature(), information.get_user_id())
        connection = pymysql.connect(host=self.__db_host, user=self.__db_admin, password=self.__db_password,
                                     database=self.__db, port=self.__port, charset=self.__charset)
        cursor = connection.cursor()
        try:
            cursor.execute(sql)
            connection.commit()
            result = 0
        except:
            traceback.print_exc()
            result = -2
        finally:
            connection.close()
            cursor.close()

        return result

    # 更新头像
    def update_avatar(self, information):
        sql = 'update information set avatar = "%s" where user_id = %s' % (information.get_avatar(), information.get_user_id())
        connection = pymysql.connect(host=self.__db_host, user=self.__db_admin, password=self.__db_password,
                                     database=self.__db, port=self.__port, charset=self.__charset)
        cursor = connection.cursor()
        try:
            cursor.execute(sql)
            connection.commit()
            result = 0
        except:
            traceback.print_exc()
            result = None
        finally:
            connection.close()
            cursor.close()

        return result

    # 更新背景
    def update_background_photo(self, information):
        sql = 'update information set background_photo = "%s" where user_id = %s' % (information.get_background_photo(), information.get_user_id())
        connection = pymysql.connect(host=self.__db_host, user=self.__db_admin, password=self.__db_password,
                                     database=self.__db, port=self.__port, charset=self.__charset)
        cursor = connection.cursor()
        try:
            cursor.execute(sql)
            connection.commit()
            result = 0
        except:
            traceback.print_exc()
            result = None
        finally:
            connection.close()
            cursor.close()

        return result

