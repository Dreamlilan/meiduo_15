from django.shortcuts import render

# Create your views here.
"""
数据库查询省份信息
select * from tb_areas where parent_id is null;
数据库查询市信息
select * from tb_areas where parent_id is 110000;
数据库查询区县信息
select * from tb_areas where parent_id is 110100;


url:
areas/infos/   查询省的信息
areas/infos/pk  查询指定市、县区信息


"""

"""
需求： 获取省的信息
1.获取查询结果集；
areas = areas.objects.filter(parent_id__isnull = True)
2.将查询结果集给序列化器；
serializer = AreaSerializer(areas,many=True)
3.返回响应；
return Response(serializer.data)
"""

"""
areas/infos/pk
需求： 获取市\区县的信息
1.获取查询结果集；
areas = areas.objects.filter(parent_id = pk)
2.将查询结果集给序列化器；
serializer = AreaSerializer(areas,many=True)
3.返回响应；
return Response(serializer.data)
"""
from rest_framework.viewsets import ReadOnlyModelViewSet
from .models import Area
from .serializers import AreaSerializer, AreaSubSerializer
from rest_framework_extensions.cache.mixins import ListCacheResponseMixin
from rest_framework_extensions.cache.mixins import RetrieveCacheResponseMixin
from rest_framework_extensions.cache.mixins import CacheResponseMixin

class AreaViewSet(CacheResponseMixin,ReadOnlyModelViewSet):

    # ReadOnlyModelViewSet继承自GenericAPIView

    # 获取所有省市区县的信息
    # queryset = Area.objects.all()
    # 获取所有省的信息
    # queryset = Area.objects.filter(parent_id__isnull = True)

    def get_queryset(self):

        if self.action == 'list':
            # 获取省的信息
            return Area.objects.filter(parent_id__isnull = True)
        else:
            # 获取市区县的信息
            return Area.objects.all()


    # serializer_class = AreaSerializer
    def get_serializer_class(self):
        if self.action == 'list':
            return AreaSerializer
        else:
            return AreaSubSerializer


from django.shortcuts import render

# Create your views here.




"""

books/ 所有书籍
books/pk/ 获取某一本书籍


areas/infos/        获取省份信息
areas/infos/pk/     市,区县信息


省份信息
select * from tb_areas where parent_id is null;


市的信息
select * from tb_areas where parent_id=110000;
区县
select * from tb_areas where parent_id=110100;




"""


"""
areas/infos/
省的信息 ,获取思路

1. 获取查询结果集
    areas = Areas.objects.filter(parent_id__isnull=True)
2. 将结果给序列化器
    serializer = AreaSerailizer(areas,many=True)
3. 返回响应
    Response(serialzier.data)

"""

"""
areas/infos/pk/
市,区县的信息 ,获取思路

1. 获取查询结果集
    areas = Areas.objects.filter(parent_id=pk)
2. 将结果给序列化器
    serializer = AreaSerailizer(areas,many=True)
3. 返回响应
    Response(serialzier.data)

"""

# from rest_framework.viewsets import ReadOnlyModelViewSet
# from .models import Area
# from .serializers import AreaSerializer,AreaSubSerializer
# from rest_framework_extensions.cache.mixins import ListCacheResponseMixin,RetrieveCacheResponseMixin
# from rest_framework_extensions.cache.mixins import CacheResponseMixin
#
# class AreaViewSet(CacheResponseMixin,ReadOnlyModelViewSet):
#     # ReadOnlyModelViewSet 最终也是继承自 GenericAPIView
#
#     # ReadOnlyModelViewSet
#
#     # queryset = Area.objects.all()
#     # queryset = Area.objects.filter(parent_id__isnull=True)
#
#     def get_queryset(self):
#
#         if self.action == 'list':
#             #获取省的信息
#             return  Area.objects.filter(parent_id__isnull=True)
#         else:
#             #获取市区县信息
#             return Area.objects.all()
#
#     # serializer_class = AreaSerailizer
#     # serializer_class = AreaSubSerializer
#
#     def get_serializer_class(self):
#         if self.action == 'list':
#             return AreaSerializer
#
#         else:
#             return AreaSubSerializer



























