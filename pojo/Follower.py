class Follower:
    __name = None
    __follower_id = None
    __avatar = None

    def set_avatar(self, avatar):
        self.__avatar = avatar
        return

    def set_name(self, name):
        self.__name = name
        return

    def set_follower_id(self, follower_id):
        self.__follower_id = follower_id
        return

    def get_name(self):
        return self.__name

    def get_follower_id(self):
        return self.__follower_id

    def get_avatar(self):
        return self.__avatar
