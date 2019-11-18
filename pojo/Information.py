from pojo.Rank import Rank


class Information:
    __user_id = None
    __nick_name = None
    __avatar = None
    __background_photo = None
    __signature = None
    __follower = 0
    __following = 0
    __rank = 1
    __my_like = None

    def set_user_id(self, user_id):
        self.__user_id = user_id
        return

    def get_user_id(self):
        return self.__user_id

    def set_my_like(self, my_like):
        self.__my_like = my_like
        return

    def set_nick_name(self, nick_name):
        self.__nick_name = nick_name
        return

    def set_avatar(self, avatar):
        self.__avatar = avatar
        return

    def set_background_photo(self, background_photo):
        self.__background_photo = background_photo
        return

    def set_signature(self, signature):
        self.__signature = signature
        return

    def set_follower(self, follower):
        self.__follower = follower
        return

    def set_following(self, following):
        self.__following = following
        return

    def set_rank(self, rank):
        self.__rank = rank
        return

    def get_nick_name(self):
        return str(self.__nick_name)

    def get_avatar(self):
        return str(self.__avatar)

    def get_background_photo(self):
        return str(self.__background_photo)

    def get_signature(self):
        return str(self.__signature)

    def get_follower(self):
        return self.__follower

    def get_following(self):
        return self.__following

    def get_rank(self):
        return Rank.get_ank(self.__rank)

    def get_my_like(self):
        return self.__my_like