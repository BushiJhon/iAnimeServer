import jwt

from dao.UserDAO import UserDAO
from pojo.User import User


class Auth:
    @staticmethod
    def encode_auth_token():
        return

    @staticmethod
    def decode_auth_token():
        return

    # 用户登录授权
    def authorize(self, phone, password):
        # 搜索是否存在用户
        user = User()
        user.set_phone(phone)
        user.set_password(password)

        user_dao = UserDAO()
        #
        return

    def identify(self):
        return