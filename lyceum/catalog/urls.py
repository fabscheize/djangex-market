from django.urls import path, re_path, register_converter

from . import converters, views

register_converter(converters.PositiveIntegerConverter, 'uint')

urlpatterns = [
    path('', views.item_list),
    path('<int:id>/', views.item_detail),
    re_path(r'^re/(?P<id>[1-9]\d*)/$', views.re_item_detail),
    path('converter/<uint:id>/', views.converter_item_detail),
]
