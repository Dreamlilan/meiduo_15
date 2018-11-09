from django.conf import settings
from django.shortcuts import render

# Create your views here.

from QQLoginTool.QQtool import OAuthQQ
from rest_framework.response import Response
from rest_framework.views import APIView

"""
QQ登陆流程：1.获取code;2.通过code换取token；3.通过token换取openid;

用户点击QQ登陆按钮，前端发送ajax请求，跳转到url
这个 url 是根据腾讯的文档生成
GET  /oauth/qq/statues/

"""

class OauthQQURLView(APIView):

    state = 'text'

    def get(self,request):

        # 1.初始化OAuthQQ对象
        oauth = OAuthQQ(client_id=settings.QQ_CLIENT_ID,
                        client_secret=settings.QQ_CLIENT_SECRET,
                        redirect_uri=settings.QQ_REDIRECT_URI)


        # 2.调用方法，获取url对象
        # 获取QQ登录扫码页面，扫码后得到Authorization Code
        login_url = oauth.get_qq_url()
        return Response({'login_url':login_url})
















