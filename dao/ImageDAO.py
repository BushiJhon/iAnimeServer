import traceback

import pymysql

from pojo.Image import Work
from dao.DatabaseConfig import *

class WorkDAO:
    __db_host = host
    __db_admin = admin
    __db_password = password
    __db = database
    __port = port
    __charset = charset

    def retrieve(self, artist):
        retrieve_works = []

        sql = 'select * from work where artist = %s' % artist
        connection = pymysql.connect(host=self.__db_host, user=self.__db_admin, password=self.__db_password,
                                     database=self.__db, port=self.__port, charset=self.__charset)
        cursor = connection.cursor()
        try:
            cursor.execute(sql)
            result = cursor.fetchall()
            if result is not None:
                for index in range(len(result)):
                    work_result = result[index]
                    work = Work()
                    work.set_id(work_result[0])
                    work.set_artist(work_result[1])
                    work.set_artist_name(work_result[2])
                    work.set_name(work_result[3])
                    work.set_created(work_result[4])
                    work.set_description(work_result[5])
                    work.set_forks(work_result[6])
                    work.set_likes(work_result[7])
                    work.set_allow_download(bool(work_result[8]))
                    work.set_allow_sketch(bool(work_result[9]))
                    work.set_allow_fork(bool(work_result[10]))
                    retrieve_works.append(work)
        except:
            traceback.print_exc()
        finally:
            connection.close()
            cursor.close()

        return retrieve_works

    # def detail_retrieve(self, artist):
    #     retrieve_works = []
    #
    #     sql = 'select * from work where artist = %s' % (artist)
    #     connection = pymysql.connect(self.__db_host, self.__db_admin, self.__db_password, self.__db, charset='utf8')
    #     cursor = connection.cursor()
    #     try:
    #         cursor.execute(sql)
    #         result = cursor.fetchall()
    #         if result is not None:
    #             for index in range(len(result)):
    #                 work_result = result[index]
    #                 work = Work()
    #                 work.set_id(work_result[0])
    #                 work.set_artist(work_result[1])
    #                 work.set_artist_name(work_result[2])
    #                 work.set_name(work_result[3])
    #                 work.set_created(work_result[4])
    #                 work.set_allow_download(work_result[5])
    #                 work.set_forks(work_result[6])
    #                 work.set_likes(work_result[7])
    #                 work.set_allow_download(work_result[8])
    #                 work.set_allow_sketch(work_result[9])
    #                 work.set_allow_fork(work_result[10])
    #                 result = {
    #                     "id": work.get_id(),
    #                     "artist": work.get_artist(),
    #                     "artist_name": work.get_artist_name(),
    #                     "name": work.get_name(),
    #                     "created": work.get_created(),
    #                     "description": work.get_description(),
    #                     "tags": work.get_tags(),
    #                     "forks": work.get_forks(),
    #                     "like": work.get_likes(),
    #                     "allow_download": work.get_description(),
    #                     "allow_sketch": work.get_allow_sketch(),
    #                     "allow_fork": work.get_allow_fork()
    #                 }
    #                 retrieve_works.append(result)
    #     except:
    #         traceback.print_exc()
    #     finally:
    #         connection.close()
    #         cursor.close()
    #
    #     return retrieve_works

    # 获取地址
    def retrieve_address(self, id):
        address = None

        sql = 'select path from address where work_id = %s' % (id)
        connection = pymysql.connect(host=self.__db_host, user=self.__db_admin, password=self.__db_password,
                                     database=self.__db, port=self.__port, charset=self.__charset)
        cursor = connection.cursor()
        try:
            cursor.execute(sql)
            result = cursor.fetchone()
            address = result[0]
        except:
            traceback.print_exc()
        finally:
            connection.close()
            cursor.close()

        return address

    # 列举
    def list(self, ids):
        my_like_works = []

        connection = pymysql.connect(host=self.__db_host, user=self.__db_admin, password=self.__db_password,
                                     database=self.__db, port=self.__port, charset=self.__charset)
        cursor = connection.cursor()
        try:
            for index in range(len(ids)):
                sql = 'select * from work where id = %s' % ids[index]
                cursor.execute(sql)
                work_result = cursor.fetchone()
                work = Work()
                work.set_id(work_result[0])
                work.set_artist(work_result[1])
                work.set_artist_name(work_result[2])
                work.set_name(work_result[3])
                work.set_created(work_result[4])
                work.set_description(work_result[5])
                work.set_forks(work_result[6])
                work.set_likes(work_result[7])
                work.set_allow_download(bool(work_result[8]))
                work.set_allow_sketch(bool(work_result[9]))
                work.set_allow_fork(bool(work_result[10]))
                my_like_works.append(work)
        except:
            traceback.print_exc()
        finally:
            connection.close()
            cursor.close()

        return my_like_works

    def retrieve_information(self, id):
        result_work = None

        sql = 'select * from work where id = %s' % id
        connection = pymysql.connect(host=self.__db_host, user=self.__db_admin, password=self.__db_password,
                                     database=self.__db, port=self.__port, charset=self.__charset)
        cursor = connection.cursor()
        try:
            cursor.execute(sql)
            result = cursor.fetchone()
            if result is not None:
                result_work = Work()
                result_work.set_id(result[0])
                result_work.set_artist(result[1])
                result_work.set_artist_name(result[2])
                result_work.set_name(result[3])
                result_work.set_created(result[4])
                result_work.set_description(result[5])
                result_work.set_forks(result[6])
                result_work.set_likes(result[7])
                result_work.set_allow_download(bool(result[8]))
                result_work.set_allow_sketch(bool(result[9]))
                result_work.set_allow_fork(bool(result[10]))
        except:
            traceback.print_exc()
        finally:
            connection.close()
            cursor.close()

        return result_work

    def add_my_like(self, user_id, work_id):
        sql = 'insert into my_like values(%s, %s)' % (user_id, work_id)
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

    def delete_my_like(self, user_id, work_id):
        sql = 'delete from my_like where user_id = %s and work_id = %s' % (user_id, work_id)
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

    def add_work(self, work, address):
        sql = 'select nick_name from information where user_id = %s' % work.get_artist()
        connection = pymysql.connect(host=self.__db_host, user=self.__db_admin, password=self.__db_password,
                                     database=self.__db, port=self.__port, charset=self.__charset)
        cursor = connection.cursor()
        try:
            cursor.execute(sql)
            result = cursor.fetchone()
            if result is not None:
                work.set_artist_name(result[0])
            sql = 'select work_id from address where original_image = "%s" and colorization_image = "%s"' % (address.get_original_image(), address.get_colorization_image())
            cursor.execute(sql)
            result = cursor.fetchone()
            if result is not None:
                work.set_id(result[0])
            sql = 'insert into work values(%s, %s, "%s", "%s", %s, "%s", %s, %s, %s, %s, %s)' % (work.get_id(), work.get_artist(), work.get_artist_name(), work.get_name(), work.get_created(), work.get_description(), work.get_forks(), work.get_likes(), work.get_allow_download(), work.get_allow_sketch(), work.get_allow_fork())
            cursor.execute(sql)
            connection.commit()
        except:
            traceback.print_exc()
        finally:
            connection.close()
            cursor.close()

        return