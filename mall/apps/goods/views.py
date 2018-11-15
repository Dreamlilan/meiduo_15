from django.shortcuts import render
from rest_framework.filters import OrderingFilter
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from goods.models import SKU
from utils.pagination import StandardResultsSetPagination
from .serializers import HotSKUSerializer

"""
伪静态化和纯静态化的区别;
纯静态化就是固定写死展示给用户的数据，但是不能满足需求；
伪静态化就是在静态化页面有部分数据是会实时变化的，比如局部信息推送或刷新；

"""
# Create your views here.


"""
需求一：获取商品列表&推荐信息
思路分析：
1.前端传递分类id,后端API接收分类id;
2.根据分类id查询商品数据，并对商品数据进行排序，并获取2个商品,[SKU,SKU,SKU]
3.对数据进行序列化操作（把数据转换成字典列表）;
4.通过JsonResponse返回数据；
GET   /goods/categories/(?P<category_id>\d+)/hotskus
"""
# 方法一：使用一级视图实现
# class HotSKUView(APIView):
#     def get(self,request,category_id):
#
#         # 1.前端传递cate_id,后端API接收分类id;
#         # 2.根据cate_id查询商品数据，并对商品数据进行排序获取2个商品;
#         # 3.有分类，需要判断上架；
#         skus = SKU.objects.filter(category_id=category_id,is_launched=True).order_by('-sales')[:2]
#         # 4.对数据进行序列化操作，将对象转换为字典；
#         serializer = HotSKUSerializer(skus,many=True)
#         # 5.返回数据
#         return Response(serializer.data)


# 方法二：
# 以上需求用三级视图实现：
class HotSKUView(ListAPIView):
    serializer_class = HotSKUSerializer
    # category_id 无法获取
    # queryset = SKU.objects.filter(category_id=category_id,is_launched=True).order_by('-sales')[:2]

    def get_queryset(self):
        # kwargs 关键字参数 args 位置参数
        # 可以在此处断点，在消息输出框会出现kwargs
        category_id = self.kwargs['category_id']

        return SKU.objects.filter(category_id=category_id, is_launched=True).order_by('-sales')[:2]


"""
需求二：列表页面数据的获取
思路分析：
1.实现返回所有分类数据；
2.实现排序；
3.实现分页；

GET  /goods/categories/(?P<category_id>\d+)/skus/?ordering=xxx&page_size=xxx&page=xxx
"""
class SKUListVIew(ListAPIView):
    # 1. 排序
    filter_backends = [OrderingFilter]
    # 设置排序字段，但在实际工作中，具体根据什么来排序要看产品经理的意思
    # 备注：1.1 排序默认是升序aesc
    ordering_fields = ['create_time','price','sales']
    # 备注：1.2 url参数 ?ordering = 字段名

    # 2.指定分页类 ???????
    # 1.分页类的设置可以放在这里，只供这一个API使用；
    # 2.也可以设置在settings配置文件中，如果其他API需要这个分页类，调用即可；
    """
    备注:二级以及二级以上视图有分页功能
    areas/views.py 省市区API继承自二级视图，查询省市区信息的时候却没有实现分页,为什么？
    答：因为我们在定义视图的视图是使用了缓存，要想实现分页，需要去redis数据库删除缓存数据，然后再去请求就可以实现省市区的信息的分页效果；
    """
    Pagination_class = StandardResultsSetPagination

    # 3.指定序列化器
    serializer_class = HotSKUSerializer

    def get_queryset(self):
        category_id = self.kwargs['category_id']

        return SKU.objects.filter(category_id=category_id, is_launched=True)





























