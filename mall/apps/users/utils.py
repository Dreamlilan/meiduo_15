from itsdangerous import TimedJSONWebSignatureSerializer as Serializer,BadSignature
from mall import settings


def generic_active_url(user_id, email):
    # token中应该含有用户信息

    # 1.创建序列化器
    serializer = Serializer(settings.SECRET_KEY, 3600)
    # 2.组织数据
    data = {
        'id': user_id,
        'email': email
    }
    # 3.对数据进行处理
    token = serializer.dumps(data)

    # 4.返回url
    return 'http://www.meiduo.site:8080/success_verify_email.html?token=' + token.decode()


from users.models import User

def get_active_user(token):

    #1.创建序列化器
    serializer = Serializer(settings.SECRET_KEY,3600)
    #2.调用序列化器的loads方法, 判断异常
    try:
       result = serializer.loads(token)
       # {id:xxx,email:xxx}
    except BadSignature:
        return None
    else:
        id = result.get('id')
        email =  result.get('email')
        # 为了让查询更准确 可以我们通过 and查询 ( where id=1 and email=123@qq.com)

        try:
            # 3. 如果获取了 id,我们再根据id进行用户的对象查询
            user = User.objects.get(id=id,email=email)
        except User.DoesNotExist:
            return None
        else:
            return user











