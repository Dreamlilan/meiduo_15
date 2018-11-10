from django.conf import settings
from QQLoginTool.QQtool import OAuthQQ
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from oauth.models import OAuthQQUser

# Create your views here.
from oauth.serializers import OauthQQUserSerializer
from oauth.utils import generic_access_token

"""
思路：
QQ登陆流程：1.获取code;2.通过code换取token；3.通过token换取openid;

用户点击QQ登陆按钮，前端发送ajax请求，跳转到url
这个 url 是根据腾讯的文档生成
GET  /oauth/qq/statues/

"""


class OauthQQURLView(APIView):
    def get(self, request):
        state = 'test'
        # 1.初始化OAuthQQ对象
        oauth = OAuthQQ(client_id=settings.QQ_CLIENT_ID,
                        client_secret=settings.QQ_CLIENT_SECRET,
                        redirect_uri=settings.QQ_REDIRECT_URI,
                        state=state)

        # 2.调用方法，获取url对象
        # 获取QQ登录扫码页面，扫码后得到Authorization Code
        login_url = oauth.get_qq_url()
        return Response({'login_url': login_url})


"""
思路：
前段应该 在用户扫描二维码/输入用户名密码登陆完成之后,跳转到 美多商城QQ绑定界面
http://www.meiduo.site:8080/oauth_callback.html?code=6E2E3F64C34ECFE29222EBC390D29196&state=test
把code传递给后端,然后用code获取token，接着用token换取openid,网站始终获取不到你的QQ和密码，openid是唯一身份识别

GET     /oauth/qq/users/?code=xxx

# 1.我们获取到这个code, 通过接口来获取 token
# 2.有了token,就可以换取 oepnid


"""


class OauthQQUserView(APIView):
    def get(self, request):
        code = request.query_params.get('code')
        if code is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        # 1. 获取到code，通过接口来获取token
        oauth = OAuthQQ(client_id=settings.QQ_CLIENT_ID,
                        client_secret=settings.QQ_CLIENT_SECRET,
                        redirect_uri=settings.QQ_REDIRECT_URI)
        # 获取token
        access_token = oauth.get_access_token(code)

        # 2. 有了token,就可以换取openid
        openid = oauth.get_open_id(access_token)

        # 3.我们需要根据openid来判断：
        # 如果数据库中openid,说明用户已经绑定过；否则没有绑定，应该显示绑定界面
        try:
            qquser = OAuthQQUser.objects.get(openid=openid)
        except OAuthQQUser.DoesNotExist:
            # openid = generic_access_token(openid)
            # 说明没有绑定过
            """
            1. 需要对敏感数据进行处理
            2. 数据还需要一个有效期
            """

            # 我们需要对 openid进行处理
            openid = generic_access_token(openid)

            return Response({'access_token': openid})
        else:
            # 没有异常走else
            # else说明用户已经绑定过，绑定过就应该显示登录；
            # 既然是登录，则应该返回token；
            from rest_framework_jwt.settings import api_settings

            # 如果openid已绑定美多商城用户，直接生成JWT token，并返回
            jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
            jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

            payload = jwt_payload_handler(qquser.user)
            token = jwt_encode_handler(payload)

            return Response({
                'user_id': qquser.user.id,
                'username': qquser.user.username,
                'token': token
            })

    """
    用户点击绑定按钮的时候,前端应该将 手机号,密码,openid,sms_code 发送给后端

    1. 接收数据
    # 2. 对数据进行校验
    #     2.1 校验 openid 和sms_code
    #     2.2 判断手机号
    #         如果注册过,需要判断 密码是否正确
    #         如果没有注册过,创建用户
    3. 保存数据
        3.1保存 user 和 openid
    4. 返回响应

    POST

    """

    def post(self, request):

        # 1. 接收数据
        data = request.data
        # 2. 对数据进行校验
        #     2.1 校验 openid 和sms_code
        #     2.2 判断手机号
        #         如果注册过,需要判断 密码是否正确
        #         如果没有注册过,创建用户
        serializer = OauthQQUserSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        # 3. 保存数据
        qquser = serializer.save()
        # 4. 返回响应
        from rest_framework_jwt.settings import api_settings

        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(qquser.user)
        token = jwt_encode_handler(payload)

        return Response({
            'user_id': qquser.user.id,
            'username': qquser.user.username,
            'token': token
        })


# 加密签名
# 使用TimedJSONWebSignatureSerializer可以生成带有有效期的token
# from itsdangerous import JSONWebSignatureSerializer # 错误的
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired
from django.conf import settings

# 1.创建 序列化器
# secret_key             秘钥,一般使用工程的 SECRET_KEY
# expires_in=None       有效期 单位秒
serializer = Serializer(settings.SECRET_KEY, 3600)

# 2. 组织 加密数据
data = {'openid': '1234567890'}

# 3.进行加密处理
token = serializer.dumps(data)

"""
eyJhbGciOiJIUzI1NiIsImV4cCI6MTU0MTc1Mzg2MCwiaWF0IjoxNTQxNzUwMjYwfQ.
eyJvcGVuaWQiOiIxMjM0NTY3ODkwIn0.
2cmQN_o0CbfsZZEqIyoHyhDmgseaNkDJ5Xqr68iFnLE

"""

# 4.对数据进行解密
# 4.对数据进行解密
serializer.loads(token)

# 5.有效期
serializer = Serializer(settings.SECRET_KEY, 1)

data = {'openid': '1234567890'}

token = serializer.dumps(data)

serializer.loads(token)
