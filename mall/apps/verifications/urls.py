from django.conf.urls import url

from apps.verifications import views

urlpatterns = [
    url(r'^imagecodes/(?P<image_code_id>.+)/$',views.RegisterImageCodeIdAPIView.as_view(),name='imagecode'),
    url(r'^smscodes/(?P<mobile>1[345789]\d{9})/$',views.RegisterSmsCodeAPIView.as_view(),name='smscode'),
]









