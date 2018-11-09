from django.conf.urls import url
from . import views
from rest_framework_jwt.views import obtain_jwt_token
urlpatterns = [
    # /users/usernames/(?P<username>\w{5,20})/count/
    url(r'^usernames/(?P<username>\w{5,20})/count/$',views.RegisterUsernameCountAPIView.as_view(),name='usernamecount'),
    url(r'^phones/(?P<mobile>1[345789]\d{9})/count/$', views.RegisterPhoneCountAPIView.as_view(),name='mobilecount'),
    url(r'^auths/$', obtain_jwt_token),

    url(r'^$', views.RegisterCreateUserView.as_view(),name='createuser'),
    # 启用通过POST获取令牌包括用户的用户名和密码

]

