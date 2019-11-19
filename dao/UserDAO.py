import traceback
import pymysql

from pojo.User import User
from dao.DatabaseConfig import *


class UserDAO:
    __db_host = host
    __db_admin = admin
    __db_password = password
    __db = database
    __port = port
    __charset = charset

    # 增加用户
    # 已修改
    def add(self, user):
        sql = 'insert into user(user_id, phone, password) values( null, "%s", "%s" )' % (
            user.get_phone(), user.get_password())
        connection = pymysql.connect(host=self.__db_host, user=self.__db_admin, password=self.__db_password,
                                     database=self.__db, port=self.__port, charset=self.__charset)
        cursor = connection.cursor()
        try:
            cursor.execute(sql)
            sql = 'select user_id from user where phone = "%s"' % user.get_phone()
            cursor.execute(sql)
            result = cursor.fetchone()
            sql = 'insert into information(user_id) values(%s)' % result[0]
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
    # 已修改
    def retrieve(self, user):
        retrieve_user = None

        if user.get_user_id() is None:
            sql = 'select * from user where phone = "%s" and password = "%s"' % (user.get_phone(), user.get_password())
        else:
            sql = 'select * from user where user_id = %s' % (user.get_user_id())
        connection = pymysql.connect(host=self.__db_host, user=self.__db_admin, password=self.__db_password,
                                     database=self.__db, port=self.__port, charset=self.__charset)
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

    # # 根据user_id查找
    # def get(self, user_id):
    #     retrieve_user = None
    #
    #     sql = 'select * from user where user_id = %s' % (user_id)
    #     connection = pymysql.connect(self.__db_host, self.__db_admin, self.__db_password, self.__db, charset='utf8')
    #     cursor = connection.cursor()
    #     try:
    #         cursor.execute(sql)
    #         result = cursor.fetchone()
    #         if result is not None:
    #             retrieve_user = User()
    #             retrieve_user.set_user_id(result[0])
    #             retrieve_user.set_phone(result[1])
    #             retrieve_user.set_password(result[2])
    #             retrieve_user.set_nick_name(result[3])
    #             retrieve_user.set_avatar(result[4])
    #             retrieve_user.set_background_photo(result[5])
    #             retrieve_user.set_signature(result[6])
    #             retrieve_user.set_rank(result[7])
    #     except:
    #         traceback.print_exc()
    #     finally:
    #         connection.close()
    #         cursor.close()
    #
    #     return retrieve_user

    # 更新
    # def update(self, user):
    #     sql = 'update user set nick_name = "%s", avatar = "%s", background_photo = "%s"' \
    #           ', signature = "%s" where user_id = %s' % (
    #               user.get_nick_name(), user.get_avatar(), user.get_background_photo(),
    #               user.get_signature(), user.get_user_id())
    #     connection = pymysql.connect(self.__db_host, self.__db_admin, self.__db_password, self.__db, charset='utf8')
    #     cursor = connection.cursor()
    #     try:
    #         cursor.execute(sql)
    #         connection.commit()
    #         result = {"StatusCode": 0}
    #     except:
    #         traceback.print_exc()
    #         result = {"StatusCode": -2}
    #     finally:
    #         connection.close()
    #         cursor.close()
    #
    #     return result

    # def update_avatar(self, user):
    #     sql = 'update user set avatar = "%s" where user_id = %s' % (user.get_avatar(), user.get_user_id())
    #     connection = pymysql.connect(self.__db_host, self.__db_admin, self.__db_password, self.__db, charset='utf8')
    #     cursor = connection.cursor()
    #     try:
    #         cursor.execute(sql)
    #         connection.commit()
    #         result = {"StatusCode": 0,
    #                   "Avatar": user.get_avatar()}
    #     except:
    #         traceback.print_exc()
    #         result = {"StatusCode": -2}
    #     finally:
    #         connection.close()
    #         cursor.close()
    #
    #     return result

    # 更新背景
    # def update_background_photo(self, user):
    #     sql = 'update user set background_photo = "%s" where user_id = %s' % (
    #         user.get_background_photo(), user.get_user_id())
    #     connection = pymysql.connect(self.__db_host, self.__db_admin, self.__db_password, self.__db, charset='utf8')
    #     cursor = connection.cursor()
    #     try:
    #         cursor.execute(sql)
    #         connection.commit()
    #         result = {"StatusCode": 0,
    #                   "Homepage": user.get_background_photo()}
    #     except:
    #         traceback.print_exc()
    #         result = {"StatusCode": -2}
    #     finally:
    #         connection.close()
    #         cursor.close()
    #
    #     return result

    # 获取我关注的作品id
    def get_my_like(self, user):
        sql = 'select work_id from my_like where user_id = %s' % (user.get_user_id())
        connection = pymysql.connect(host=self.__db_host, user=self.__db_admin, password=self.__db_password,
                                     database=self.__db, port=self.__port, charset=self.__charset)
        cursor = connection.cursor()
        try:
            cursor.execute(sql)
            result = cursor.fetchall()
            work_id = []
            if result is not None:
                for index in range(len(result)):
                    work_id.append(result[index][0])
        except:
            traceback.print_exc()
        finally:
            connection.close()
            cursor.close()

        return work_id

