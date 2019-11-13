from datetime import datetime, timedelta

import jwt

class Auth:
    @staticmethod
    def encode_auth_token(now_time, exp_time, id):
        try:
            payload = {
                'exp': exp_time,
                'iat': now_time,
                'user_id': id
            }
            return jwt.encode(
                payload,
                'SECRET_KEY',
                algorithm='HS256'
            )
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token():

        return

    # 用户登录授权
    def authorize(self, user):
        now_time = datetime.utcnow()
        exp_time = now_time + timedelta(days=1)

        Token = Auth.encode_auth_token(now_time, exp_time, user.get_user_id())
        result = {
            "StatusCode": 0,
            "Token": Token.decode(),
            "TokenExpire": exp_time
        }
        return result

    def identify(self):
        return

Auth().decode_auth_token()