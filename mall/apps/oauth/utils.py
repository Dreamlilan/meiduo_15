#coding:utf8
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer,BadSignature,SignatureExpired
from mall import settings


def generic_access_token(openid):
    # 生成序列化器
    serializer = Serializer(settings.SECRET_KEY,3600)
    # 对敏感数据进校验
    token = serializer.dumps({'openid':openid})
    # 返回数据
    return token.decode()

def check_open_id(token):
    # 生成序列化器
    serializer = Serializer(settings.SECRET_KEY, 3600)
    # 校验
    try:
        result = serializer.loads(token)
        # result 就应该是当时 加密的数据
    except BadSignature:
        return None
    else:
        return result.get('openid')


