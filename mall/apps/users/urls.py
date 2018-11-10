from django.conf.urls import url
from . import views
from rest_framework_jwt.views import obtain_jwt_token
urlpatterns = [
    # /users/usernames/(?P<username>\w{5,20})/count/
    url(r'^usernames/(?P<username>\w{5,20})/count/$',views.RegisterUsernameCountAPIView.as_view(),name='usernamecount'),
    url(r'^phones/(?P<mobile>1[345789]\d{9})/count/$', views.RegisterPhoneCountAPIView.as_view(),name='mobilecount'),
    url(r'^auths/$', obtain_jwt_token),

    url(r'^$', views.RegisterCreateUserView.as_view(),name='createuser'),

    # /users/infos/
    url(r'^infos/$',views.UserCenterView.as_view()),
    # /users/emails/
    url(r'^emails/$',views.UserEmailView.as_view()),

]

