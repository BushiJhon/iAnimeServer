import traceback

import pymysql

from pojo.Follower import Follower


class FollowerDAO:
    __db_host = '127.0.0.1'
    __db_admin = 'root'
    __db_password = 'root'
    __db = 'iAnimeSQL'

    def retrieve(self, user_id):
        retrieve_followers = None

        sql = 'select * from id_followerId where user_id = %s' % (user_id)
        connection = pymysql.connect(self.__db_host, self.__db_admin, self.__db_password, self.__db, charset='utf8')
        cursor = connection.cursor()
        try:
            cursor.execute(sql)
            result = cursor.fetchall()
            if result is not None:
                retrieve_followers = []
                for index in range(len(result)):
                    follower_result = result[index]
                    follower = Follower()
                    follower.set_follower_id(follower_result[1])
                    retrieve_followers.append(follower)
        except:
            traceback.print_exc()
        finally:
            connection.close()
            cursor.close()

        return retrieve_followers

    # 获取完整followers
    def get(self, followers):
        connection = pymysql.connect(self.__db_host, self.__db_admin, self.__db_password, self.__db, charset='utf8')
        cursor = connection.cursor()
        results = []

        try:
            for index in range(len(followers)):
                sql = 'select * from user where user_id = %s' % (followers[index].get_follower_id())
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

# follower_dao = FollowerDAO()
# print(follower_dao.retrieve(1))