from django.urls import path

from . import views

app_name = 'ledger'
urlpatterns = [
    path('', views.view_index, name='index'),
]
