from django.conf.urls import url

from goods import views

urlpatterns = [
    url(r'^categories/(?P<category_id>\d+)/hotskus/$', views.HotSKUView.as_view(), name='hot'),
    url(r'^categories/(?P<category_id>\d+)/skus/$',views.SKUListVIew.as_view(),name='list'),
]