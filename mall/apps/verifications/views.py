# Create your views here.
from django.http import HttpResponse
from django_redis import get_redis_connection
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.views import APIView

from libs.captcha.captcha import captcha

"""
1.接收前端法发送的uuid；
2.生成图片验证码； (通过第三方库,生成图片image和验证码text,我们需要对验证码进行redis保存)
3.连接redis,保存uuid和图片验证码上面的数据； (通过redis进行保存验证码,需要在设置中添加 验证码数据库选项)
4.返回响应；( 注意,图片是二进制,我们通过HttpResponse返回)
"""


class RegisterImageCodeIdAPIView(APIView):
    """
    GET : /verifications/(?P<image_code_id>.+)/
    """

    def get(self, request, image_code_id):
        # 1.生成图片验证码
        text, image = captcha.generate_captcha()

        # 2.连接redis，保存数据
        redis_conn = get_redis_connection('code')
        from . import constant
        redis_conn.setex('img_%s' % image_code_id, constant.IMAGE_CODE_EXPIRE_TIME, text)

        # 3.返回响应

        return HttpResponse(image, content_type='image/jpeg')


"""
1.接收前端数据(用户点击获取短信验证码按钮，前端将mobile,text和uuid(即：image_code_id) 发送给后端)
2.校验数据，交给序列化器去完成；
3.生成短信验证码，发送短信；
4.返回响应；
"""

from .serializers import RegisterSmsCodeSerializer
from libs.yuntongxun.sms import CCP

class RegisterSmsCodeAPIView(APIView):
    """
    GET : /verifications/sms_codes/(?P<mobile>1[3-9]\d{9})/?uuid=xxx&text=xxx
    """

    def get(self, request, mobile):
        # 1.接收前端数据
        params = request.query_params
        # 2.校验数据，交给序列化器
        # 创建 序列化器对象
        serializer = RegisterSmsCodeSerializer(data=params)
        serializer.is_valid(raise_exception=True)
        # 3.生成短信验证码
        from random import randint
        sms_code = '%06d'%randint(0,999999)
        # 4.保存短信，发送短信
        redis_conn = get_redis_connection('code')
        redis_conn.setex('sms_%s'%mobile,300,sms_code)

        # CCP().send_template_sms(mobile,[sms_code,5],1)
        from celery_tasks.sms.tasks import send_sms_code
        send_sms_code.delay(mobile,sms_code)

        # 5.返回响应
        return Response({'msg':'ok'})




