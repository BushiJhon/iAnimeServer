class Following:
    __name = None
    __following_id = None
    __avatar = None

    def set_avatar(self, avatar):
        self.__avatar = avatar
        return

    def set_name(self, name):
        self.__name = name
        return

    def set_following_id(self, following_id):
        self.__following_id = following_id
        return

    def get_name(self):
        return self.__name

    def get_following_id(self):
        return self.__following_id

    def get_avatar(self):
        return self.__avatar

