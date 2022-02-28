from django.urls import path

from . import views

app_name = 'ledger'
urlpatterns = [
    path('', views.view_index, name='index'),

    path('stock/', views.view_stock, name='view_stock'),
    path('funds/', views.view_funds, name='view_funds'),

    path('products/search/', views.product_search, name='product_search'),

    path('accounts/', views.table_accounts, name='accounts'),
    path('account/add/', views.AccountCreate.as_view(), name='account_add'),
    path('account/<int:pk>/', views.AccountUpdate.as_view(), name='account_edit'),
    path('account/<int:pk>/delete/', views.AccountDelete.as_view(), name='account_delete'),

    path('counterparties/', views.table_counterparties, name='counterparties'),
    path('counterparty/add/', views.CounterpartyCreate.as_view(), name='counterparty_add'),
    path('counterparty/<int:pk>/', views.CounterpartyUpdate.as_view(), name='counterparty_edit'),
    path('counterparty/<int:pk>/delete/', views.CounterpartyDelete.as_view(), name='counterparty_delete'),

    path('customer_orders/', views.table_customer_orders, name='customer_orders'),
    path('customer_order/add/', views.CustomerOrderCreate.as_view(), name='customer_order_add'),
    path('customer_order/<int:pk>/', views.CustomerOrderUpdate.as_view(), name='customer_order_edit'),
    path('customer_order/<int:pk>/delete/', views.CustomerOrderDelete.as_view(), name='customer_order_delete'),

    path('customer_order_positions/', views.table_customer_order_positions, name='customer_order_positions'),
    path('customer_order_positions/action', views.CustomerOrderPositionAction.as_view(),
         name='customer_order_position_action'),
    path('customer_order_positions/delete', views.CustomerOrderPositionDelete.as_view(),
         name='customer_order_position_delete'),

    path('customer_order_payments/', views.table_customer_order_payments, name='customer_order_payments'),
    path('customer_order_payments/action', views.CustomerOrderPaymentAction.as_view(),
         name='customer_order_payment_action'),
    path('customer_order_payments/delete', views.CustomerOrderPaymentDelete.as_view(),
         name='customer_order_payment_delete'),
]
