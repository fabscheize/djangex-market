from django.urls import path, re_path, register_converter

from catalog import converters, views


app_name = 'catalog'

register_converter(converters.PositiveIntegerConverter, 'uint')

urlpatterns = [
    path('', views.item_list, name='list'),
    path('<int:pk>/', views.item_detail, name='item'),
    re_path(r'^re/(?P<pk>\d+)/$', views.item_detail, name='re_item'),
    path('converter/<uint:pk>/', views.item_detail, name='c_item'),
]
