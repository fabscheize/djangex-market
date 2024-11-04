from django.urls import path

from catalog import views


app_name = 'catalog'

urlpatterns = [
    path('', views.item_list, name='list'),
    path('<int:pk>/', views.item_detail, name='item'),
    path('new/', views.new_list, name='new'),
    path('friday/', views.friday_list, name='friday'),
    path('unverified/', views.unverified_list, name='unverified'),
]
