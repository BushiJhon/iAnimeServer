import traceback
import pymysql


class UserDAO:
    __db_host = '127.0.0.1'
    __db_admin = 'root'
    __db_password = '5257107'
    __db = 'iAnimeSQL'

    # 执行SQL语句
    def __execute_SQL(self, sql):
        db = pymysql.connect(self.__db_host, self.__db_admin, self.__db_password, self.__db)
        cursor = db.cursor()
        try:
            cursor.execute(sql)
            db.commit()
        except:
            traceback.print_exc()
            db.rollback()
        db.close()

    # 增加用户
    def add(self, user):
        sql = 'insert into user(user_id, phone, password) values( null, %s, "%s" )' % (user.get_phone(), user.get_password())
        self.__execute_SQL(self, sql)
        return

    # 查找
    def retrieve(self, user):
        sql = ''
        self.__execute_SQL(self, sql)
        return

