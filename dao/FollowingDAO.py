import traceback

import pymysql

from pojo.Following import Following


class FollowingDAO:
    __db_host = '127.0.0.1'
    __db_admin = 'root'
    __db_password = 'root'
    __db = 'iAnimeSQL'

    def retrieve(self, follower_id):
        retrieve_followings = None

        sql = 'select * from id_followerId where follower_id = %s' % (follower_id)
        connection = pymysql.connect(self.__db_host, self.__db_admin, self.__db_password, self.__db, charset='utf8')
        cursor = connection.cursor()
        try:
            cursor.execute(sql)
            result = cursor.fetchall()
            if result is not None:
                retrieve_followings = []
                for index in range(len(result)):
                    following_result = result[index]
                    following = Following()
                    following.set_following_id(following_result[0])
                    retrieve_followings.append(following)
        except:
            traceback.print_exc()
        finally:
            connection.close()
            cursor.close()

        return retrieve_followings

    # 获取完整followings
    def get(self, followings):
        connection = pymysql.connect(self.__db_host, self.__db_admin, self.__db_password, self.__db, charset='utf8')
        cursor = connection.cursor()
        results = []

        try:
            for index in range(len(followings)):
                sql = 'select * from user where user_id = %s' % (followings[index].get_following_id())
                cursor.execute(sql)
                retrieve_user = cursor.fetchone()
                result = {
                    "NickName": retrieve_user[3],
                    "UserID": retrieve_user[0],
                    "Avatar": retrieve_user[4],
                }
                results.append(result)
            return results
        except:
            traceback.print_exc()
        finally:
            connection.close()
            cursor.close()

# following_dao = FollowingDAO()
# print(following_dao.retrieve(1).pop(0).get_following_id())