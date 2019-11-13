
class User:
    __phone = None
    __password = None
    __user_id = None

    def set_user_id(self, user_id):
        self.__user_id = user_id
        return

    def set_phone(self, phone):
        self.__phone = phone
        return

    def set_password(self, password):
        self.__password = password
        return

    def get_phone(self):
        return self.__phone

    def get_password(self):
        return self.__password

    def get_user_id(self):
        return self.__user_id
