import traceback

import pymysql

from pojo.Image import Work


class WorkDAO:
    __db_host = '127.0.0.1'
    __db_admin = 'root'
    __db_password = 'root'
    __db = 'iAnimeSQL'

    def home_retrieve(self, artist):
        retrieve_works = []

        sql = 'select * from work where artist = %s' % (artist)
        connection = pymysql.connect(self.__db_host, self.__db_admin, self.__db_password, self.__db, charset='utf8')
        cursor = connection.cursor()
        try:
            cursor.execute(sql)
            result = cursor.fetchall()
            if result is not None:
                for index in range(len(result)):
                    work = result[index]
                    result = {
                        "id": work[0],
                        "name": work[3],
                        "created": work[4],
                        "artist_name": work[2]
                    }
                    retrieve_works.append(result)
        except:
            traceback.print_exc()
        finally:
            connection.close()
            cursor.close()

        return retrieve_works

    def detail_retrieve(self, artist):
        retrieve_works = []

        sql = 'select * from work where artist = %s' % (artist)
        connection = pymysql.connect(self.__db_host, self.__db_admin, self.__db_password, self.__db, charset='utf8')
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
                    work.set_allow_download(work_result[5])
                    work.set_forks(work_result[6])
                    work.set_likes(work_result[7])
                    work.set_allow_download(work_result[8])
                    work.set_allow_sketch(work_result[9])
                    work.set_allow_fork(work_result[10])
                    result = {
                        "id": work.get_id(),
                        "artist": work.get_artist(),
                        "artist_name": work.get_artist_name(),
                        "name": work.get_name(),
                        "created": work.get_created(),
                        "description": work.get_description(),
                        "tags": work.get_tags(),
                        "forks": work.get_forks(),
                        "like": work.get_likes(),
                        "allow_download": work.get_description(),
                        "allow_sketch": work.get_allow_sketch(),
                        "allow_fork": work.get_allow_fork()
                    }
                    retrieve_works.append(result)
        except:
            traceback.print_exc()
        finally:
            connection.close()
            cursor.close()

        return retrieve_works

    # 获取地址
    def retrieve_address(self, id):
        address = None

        sql = 'select address from work where id = %s' % (id)
        connection = pymysql.connect(self.__db_host, self.__db_admin, self.__db_password, self.__db, charset='utf8')
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

