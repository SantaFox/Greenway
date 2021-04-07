from django.urls import path

from . import views

app_name = 'products'
urlpatterns = [
    # TODO: надо добавить проверку на POST
    path('change_lang/', views.change_lang, name='change_lang'),
    path('', views.list_all, name='list_all'),
    path('<str:blackbox>/', views.product_dispatch, name='product'),
]
