

def jwt_response_payload_handler(token, user=None, request=None):
    #  jwt 的token
    # user 就是已经认证之后的用户信息
    return {
        'token': token,
        'username': user.username,
        'user_id': user.id
    }


import re
from users.models import User
from django.contrib.auth.backends import ModelBackend

"""

1. 登录是采用的jWT的认证方式, JWT的认证方式是在 rest_framework的基础上做的,也就是说
    JWT 其实就用的 rest_framework 的认证,只不过返回的是 token
    JWT 其实就用的 rest_framework 的认证 , rest_framework 的认证 是根据用户名来判断的

2. 我们需要判断 用户是输入的手机号还是用户名


"""


def get_user(username):
    try:
        if re.match('1[3-9]\d{9}', username):
            # 手机号
            user = User.objects.get(mobile=username)
        else:
            # 用户名
            user = User.objects.get(username=username)
    except User.DoesNotExist:
        return None

    return user


class MobileUsernameModelBackend(ModelBackend):
    """
    自定义用户名或手机号认证
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        user = get_user(username)
        # 校验用户的密码
        if user is not None and user.check_password(password):
            return user
