from django.conf import settings
from QQLoginTool.QQtool import OAuthQQ
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


# Create your views here.

"""
思路：
QQ登陆流程：1.获取code;2.通过code换取token；3.通过token换取openid;

用户点击QQ登陆按钮，前端发送ajax请求，跳转到url
这个 url 是根据腾讯的文档生成
GET  /oauth/qq/statues/

"""


class OauthQQURLView(APIView):
    def get(self, request):
        state = '/'
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

        pass