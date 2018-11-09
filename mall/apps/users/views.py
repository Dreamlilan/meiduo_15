from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from users.models import User
from apps.users.serializer import RegisterCreateUserSerializer
from rest_framework_jwt.utils import jwt_response_payload_handler

# 创建用户名视图
class RegisterUsernameCountAPIView(APIView):
    """
    获取用户名的个数
    GET:  /users/usernames/(?P<username>\w{5,20})/count/
    """

    def get(self,request,username):

        #通过模型查询,获取用户名个数
        count = User.objects.filter(username=username).count()
        #组织数据
        context = {
            'count':count,
            'username':username
        }
        return Response(context)


class RegisterPhoneCountAPIView(APIView):
    """
    查询手机号的个数
    GET ： /users/phones/(?P<mobile>1(345789)\d{9})/count/
    """
    def get(self,request,mobile):

        # 1. 通过模型类查询获取手机号个数
        count = User.objects.filter(mobile=mobile).count()

        #  2. 组织数据
        context = {
            'count':count,
            'mobile':mobile
        }

        # 3. 返回响应
        return Response(context)


"""
1.接收前端发送的数据(username,password,password2,mobile,sms_code,allow)
2.校验数据
3.数据入库
4.返回响应
"""
class RegisterCreateUserView(APIView):
    def post(self,request):
        # 1.接收前段提交的数据
        # username = request.form.get('usernmae')
        # username = request.form.get('usernmae')
        # username = request.form.get('usernmae')
        data = request.data
        # 2.校验数据
        # if not all([]):
        #     pass
        #
        serializer = RegisterCreateUserSerializer(data=data)

        serializer.is_valid(raise_exception=True)
        # 3.数据入库
        serializer.save()
        # 4.返回响应
        return Response(serializer.data)









