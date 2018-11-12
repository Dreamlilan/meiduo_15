from areas import views
from rest_framework.routers import DefaultRouter

urlpatterns = [

]


# 创建router
router = DefaultRouter()

# 设置url
router.register(r'infos',views.AreaViewSet,base_name='')

# 需要把生成的url添加到urlpatterns
urlpatterns += router.urls














