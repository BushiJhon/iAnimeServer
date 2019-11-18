
from datetime import datetime, timedelta, timezone

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
    def decode_auth_token(auth_token):
        try:
            payload = jwt.decode(auth_token, 'SECRET_KEY', options={'verify_exp': True})
            return payload
        except jwt.ExpiredSignatureError:
            return 'Token过期'
        except jwt.InvalidTokenError:
            return '无效Token'
        return

    # 用户登录授权
    @staticmethod
    def authorize(user):
        now_time = datetime.now(timezone.utc)
        exp_time = now_time + timedelta(days=1)

        now_time = now_time.timestamp()
        exp_time = exp_time.timestamp()

        Token = Auth.encode_auth_token(now_time, exp_time, user.get_user_id())
        result = {
            "StatusCode": 0,
            "Token": Token.decode(),
            "TokenExpire": int(exp_time)
        }
        return result

    # 认证
    @staticmethod
    def identify(authorization):
        if authorization is not None:
            authorization = authorization.split(' ')
            if len(authorization) != 2 or authorization[0] != 'Bearer':
                return None
            else:
                payload = Auth.decode_auth_token(authorization[1])
                if 'user_id' not in payload:
                    return None
                else:
                    return payload['user_id']
        else:
            return None


# now_time = datetime.now(timezone.utc)
# exp_time = now_time + timedelta(days=10)
#
# now_time = now_time.timestamp()
# exp_time = exp_time.timestamp()
# payload = {
#                 'exp': exp_time,
#                 'iat': now_time,
#                 'user_id': 1
#             }
# token = jwt.encode(
#                 payload,
#                 'SECRET_KEY',
#                 algorithm='HS256'
#             )
#
# print(token.decode())
