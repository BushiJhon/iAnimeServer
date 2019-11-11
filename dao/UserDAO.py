import traceback
import pymysql


class UserDAO:
    __db_host = '127.0.0.1'
    __db_admin = 'root'
    __db_password = '5257107'
    __db = 'iAnimeSQL'

    # 注册操作
    def login(self, user):
        db = pymysql.connect(self.__db_host, self.__db_admin, self.__db_password, self.__db)
        cursor = db.cursor()
        sql = 'insert into user(user_id, phone, password) values( null, %s, "%s" )'%(user.get_phone(), user.get_password())
        try:
            cursor.execute(sql)
            db.commit()
        except:
            traceback.print_exc()
            db.rollback()
        db.close()
        return
