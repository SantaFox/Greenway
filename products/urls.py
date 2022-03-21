from django.urls import path

from . import views

app_name = 'products'
urlpatterns = [
    # TODO: надо добавить проверку на POST
    path('change_lang/', views.change_lang, name='change_lang'),
    path('', views.list_products, name='list_all'),
    path('<str:blackbox>/edit/', views.edit_product, name='edit_product'),
    path('<str:blackbox>/', views.product_dispatch, name='product'),
]
