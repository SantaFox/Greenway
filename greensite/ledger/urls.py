from django.urls import path

from . import views

app_name = 'ledger'
urlpatterns = [
    path('', views.view_index, name='index'),
    path('counterparties/', views.table_counterparties, name='counterparties'),
    path('accounts/', views.table_accounts, name='accounts'),
]
