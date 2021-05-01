from django.urls import path

from . import views

app_name = 'ledger'
urlpatterns = [
    path('', views.view_index, name='index'),

    path('accounts/', views.table_accounts, name='accounts'),
    path('accounts/action/', views.account_action, name='account_action'),
    path('accounts/delete/', views.account_delete, name='account_delete'),

    path('counterparties/', views.table_counterparties, name='counterparties'),
    path('counterparties/action/', views.counterparty_action, name='counterparty_action'),
    path('counterparties/delete/', views.counterparty_delete, name='counterparty_delete'),

    path('customer_orders/', views.table_customer_orders, name='customer_orders'),
    path('customer_orders/action/', views.customer_order_action, name='customer_order_action'),
    path('customer_orders/delete/', views.customer_order_delete, name='customer_order_delete'),
]
