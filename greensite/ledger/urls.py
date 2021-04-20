from django.urls import path

from . import views

app_name = 'ledger'
urlpatterns = [
    path('', views.view_index, name='index'),
    path('accounts/', views.table_accounts, name='accounts'),
    path('counterparties/', views.table_counterparties, name='counterparties'),
    path('customer_orders/', views.table_customer_orders, name='customer_orders'),
]
