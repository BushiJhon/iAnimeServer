import traceback

import pymysql

from pojo.Following import Following

from dao.DatabaseConfig import *

class FollowingDAO:
    __db_host = host
    __db_admin = admin
    __db_password = password
    __db = database
    __port = port
    __charset = charset

    def retrieve(self, follower_id):
        retrieve_followings = []

        sql = 'select user_id from follow where follower_id = %s' % follower_id
        connection = pymysql.connect(host=self.__db_host, user=self.__db_admin, password=self.__db_password,
                                     database=self.__db, port=self.__port, charset=self.__charset)
        cursor = connection.cursor()
        try:
            cursor.execute(sql)
            result = cursor.fetchall()
            if result is not None:
                for index in range(len(result)):
                    following_result = result[index]
                    following = Following()
                    following.set_following_id(following_result[0])
                    sql = 'select avatar, nick_name from information where user_id = %s' % following.get_following_id()
                    cursor.execute(sql)
                    sub_result = cursor.fetchone()
                    following.set_avatar(sub_result[0])
                    following.set_name(sub_result[1])
                    retrieve_followings.append(following)
        except:
            traceback.print_exc()
        finally:
            connection.close()
            cursor.close()

        return retrieve_followings

    # 获取完整followings
    # def get(self, followings):
    #     connection = pymysql.connect(self.__db_host, self.__db_admin, self.__db_password, self.__db, charset='utf8')
    #     cursor = connection.cursor()
    #     results = []
    #
    #     try:
    #         for index in range(len(followings)):
    #             sql = 'select * from user where user_id = %s' % (followings[index].get_following_id())
    #             cursor.execute(sql)
    #             retrieve_user = cursor.fetchone()
    #             result = {
    #                 "NickName": retrieve_user[3],
    #                 "UserID": retrieve_user[0],
    #                 "Avatar": retrieve_user[4],
    #             }
    #             results.append(result)
    #         return results
    #     except:
    #         traceback.print_exc()
    #     finally:
    #         connection.close()
    #         cursor.close()

# following_dao = FollowingDAO()
# print(following_dao.retrieve(1).pop(0).get_following_id())