from django_redis import get_redis_connection
from rest_framework import serializers


class RegisterSmsCodeSerializer(serializers.Serializer):

    text = serializers.CharField(label='图片验证码',min_length=4,max_length=4,required=True)
    image_code_id = serializers.UUIDField(label='uuid',required=True)

    """
    校验方法:
        1.字段类型；2.字段选项；3.单个字段；4.多个字段

        校验图片验证码的时候 需要用到 text 和 image_code_id 这2个字段,所以选择 多个字段校验
    """
    def validate(self, attrs):

        # 1. 用户提交的图片验证码
        text = attrs.get('text')
        image_code_id = attrs.get('image_code_id')

        # 2.获取redis验证码
        # 2.1 获取 之前存储在redis数据库的uuid
        redis_conn = get_redis_connection('code')
        redis_text = redis_conn.get('img_%s'%image_code_id)
        # 2.2  判断uuid是否过期：
        if redis_text is None:
            raise serializers.ValidationError('图片验证码已过期')
        # 3.比较前端提交的图片验证码uuid和存储在redis数据库的uuid是否一致
        if redis_text.decode().lower() != text.lower():
            raise serializers.ValidationError('图片验证码不一致')

        # 4.校验完成，返回attrs
        return attrs






















