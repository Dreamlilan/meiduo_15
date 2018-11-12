# coding:utf8
from rest_framework import serializers

from .models import Area


# 暂时理解为省的序列化器
class AreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = ['id', 'name']


class AreaSubSerializer(serializers.ModelSerializer):
    # 这个是 市的序列化器

    subs = AreaSerializer(many=True)

    class Meta:
        model = Area
        fields = ['id', 'name', 'subs']
