from django.urls import path, re_path, register_converter

from catalog import converters, views


register_converter(converters.PositiveIntegerConverter, 'uint')

urlpatterns = [
    path('', views.item_list),
    path('<int:pk>/', views.item_detail),
    re_path(r'^re/(?P<pk>\d*[1-9]\d*)/$', views.item_detail),
    path('converter/<uint:pk>/', views.item_detail),
]
