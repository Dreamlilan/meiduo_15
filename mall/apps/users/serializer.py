# coding:utf8
import re

from django_redis import get_redis_connection
from rest_framework import serializers
from rest_framework_jwt.settings import api_settings
from users.models import User

# serializers.ModelSerializer
# serializers.Serializer

# 数据入库 选择 ModelSerializer 肯定有 模型


class RegisterCreateUserSerializer(serializers.ModelSerializer):
    """
    6个参数(username,password,password2,mobile,sms_code,allow)

    """

    sms_code = serializers.CharField(label='短信验证码', min_length=6, max_length=6, required=True,write_only=True)
    password2 = serializers.CharField(label='确认密码', required=True,write_only=True)
    allow = serializers.CharField(label='同意操作', required=True,write_only=True)
    token = serializers.CharField(label='登录状态token', read_only=True)  # 增加token字段

    # ModelSerializer 自动生成字段的时候 是根据 fields 列表来生成的
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'mobile', 'password2', 'sms_code', 'allow','token')
        extra_kwargs = {
            'id': {'read_only': True},
            'username': {
                'min_length': 5,
                'max_length': 20,
                'error_messages': {
                    'min_length': '仅允许5-20个字符的用户名',
                    'max_length': '仅允许5-20个字符的用户名',
                }
            },
            'password': {
                'write_only': True,
                'min_length': 8,
                'max_length': 20,
                'error_messages': {
                    'min_length': '仅允许8-20个字符的密码',
                    'max_length': '仅允许8-20个字符的密码',
                }
            }
        }

    """
    -->-->-->手机号校验,密码一致,短信校验,是否同意
    手机号就是规则 --> 单个字段
    是否同意 --> 单个字段
    密码一致,短信校验 --> 多个字段
    """

    # 校验手机号
    def validate_mobile(self, value):

        if not re.match('1[3-9]\d{9}', value):
            raise serializers.ValidationError('手机号不满足规则')
        # 校验之后最终要返回回去
        return value

    # 校验是否同意
    def validate_allow(self, value):

        if value == 'false':
            raise serializers.ValidationError('您未同意协议')

        return value

    # 多字段校验, 密码是否一致, 短信是否一致
    def validate(self, attrs):

        # 1 比较密码
        password = attrs['password']
        password2 = attrs['password2']

        if password != password2:
            raise serializers.ValidationError('密码不一致')
        # 2 比较手机验证码
        # 2.1获取用户提交的验证码
        code = attrs['sms_code']
        # 2.2获取redis中的验证码
        redis_conn = get_redis_connection('code')
        # 2.3获取手机号码
        mobile = attrs['mobile']
        redis_code = redis_conn.get('sms_%s' % mobile)
        if redis_code is None:
            raise serializers.ValidationError('验证码过期')

        if redis_code.decode() != code:
            raise serializers.ValidationError('验证码不正确')

        return attrs

    """
    我们添加的三个字段只是用于验证,不应该入库,
    所以我们应该在他们入库前删除,入库的时候调用create方法,于是我们重写create方法
    """

    def create(self, validated_data):

        # 删除多余字段
        del validated_data['password2']
        del validated_data['sms_code']
        del validated_data['allow']

        user = super().create(validated_data)

        # 调用django的认证系统加密密码
        user.set_password(validated_data['password'])
        user.save()

        # 补充生成记录登录状态的token
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)

        user.token = token



        return user


# 用户中心序列化器
class UserCenterSerializer(serializers.ModelSerializer):

    """
    用户详细信息序列化器
    """
    class Meta:
        model = User
        fields = ('id', 'username', 'mobile', 'email','email_active')


class UserEmailSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email',)













