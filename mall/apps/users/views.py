from django.shortcuts import render

# Create your views here.

from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from users.models import User
from apps.users.serializer import RegisterCreateUserSerializer, UserCenterSerializer
from rest_framework_jwt.utils import jwt_response_payload_handler

# 创建用户名视图
from users.utils import generic_active_url


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



# 使用一级视图
# GET     /users/infos
class UserCenterView(APIView):

    # 1. 添加权限
    permission_classes = [IsAuthenticated]

    def get(self,request):

        # 2. 获取用户信息
        user = request.user

        # 3.返回数据
        serializer = UserCenterSerializer(user)

        return Response(serializer.data)




# 使用三级视图
# from rest_framework.generics import RetrieveAPIView
#
# class UserCenterView(RetrieveAPIView):
#     # 指定序列化器
#     serializer_class = UserCenterSerializer
#     queryset = User.objects.all()
#
#     # 权限
#     permission_classes = [IsAuthenticated]
#
#     def get_object(self):
#         # 获取某一个指定的对象
#         return self.request.user


"""
需求分析：
1.用户在点击设置的时候，输入邮箱信息，点击保存，把邮箱信息发送给后端；
2.这个接口必须是登陆用户；
3.接受参数；
4.验证数据；
5.更新数据；
6.发送激活邮件；
7.返回成功响应；

PUT  /users/emails/
"""

from .serializer import UserEmailSerializer

class UserEmailView(APIView):

    # 1.这个接口必须是登陆用户；
    permission_classes = [IsAuthenticated]

    def put(self, request):

        # 2.接收参数
        data = request.data
        user = request.user

        # 3.验证数据
        serializer = UserEmailSerializer(instance=user,data=data)
        serializer.is_valid(raise_exception=True)
        # 4.更新数据
        serializer.save()
        # 5.发送激活邮件
        from django.core.mail import send_mail
        """
        send_mail( subject , message , from_email , recipient_list , html_message=None )
        subject 邮件标题
        message 普通邮件正文， 普通字符串
        from_email 发件人
        recipient_list 收件人列表
        html_message 多媒体邮件正文，可以是html字符串
        """
        subject = '美多商城'
        message = ''
        from_email = '18834078298@163.com'
        email = data.get('email')
        recipient_list = [email]
        # 可以设置以下 html的样式等信息
        verify_url = generic_active_url(user.id,email)
        html_message = '<p>尊敬的用户您好！</p>' \
                   '<p>感谢您使用美多商城。</p>' \
                   '<p>您的邮箱为：%s 。请点击此链接激活您的邮箱：</p>' \
                   '<p><a href="%s">%s<a></p>' % (email, verify_url, verify_url)
        send_mail(subject=subject,
                  message=message,
                  from_email=from_email,
                  recipient_list=recipient_list,
                  html_message=html_message
                  )


        # 6.返回响应
        return Response(serializer.data)












