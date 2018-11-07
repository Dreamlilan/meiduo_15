from django.conf.urls import url

from apps.verifications import views

urlpatterns = [
    url(r'^imagecodes/(?P<image_code_id>.+)/$',views.RegisterImageCodeIdAPIView.as_view(),name='imagecode'),
]









