import traceback

import pymysql

from dao.DatabaseConfig import *


class AddressDAO:
    __db_host = host
    __db_admin = admin
    __db_password = password
    __db = database
    __port = port
    __charset = charset

    def add(self, address):
        sql = 'insert into address values(%s, "%s", "%s", "%s", %s, "%s")' % (address.get_work_id(), address.get_path(),
                                                                        address.get_original_image(), address.get_colorization_image(),
                                                                        address.get_user_id(), address.get_receipt())
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

    def retrieve(self, address):
        sql = 'select path, colorization_image from address where receipt = "%s"' % (address.get_receipt())
        connection = pymysql.connect(host=self.__db_host, user=self.__db_admin, password=self.__db_password,
                                     database=self.__db, port=self.__port, charset=self.__charset)
        cursor = connection.cursor()
        try:
            cursor.execute(sql)
            result = cursor.fetchone()
            if result is not None:
                address.set_path(result[0])
                address.set_colorization_image(result[1])
            else:
                address = None
        except:
            traceback.print_exc()
            connection.rollback()
        finally:
            connection.close()
            cursor.close()
        return address
