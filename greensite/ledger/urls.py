from django.urls import path

from . import views

app_name = 'ledger'
urlpatterns = [
    path('', views.view_index, name='index'),
    path('accounts/', views.table_accounts, name='accounts'),
    path('accounts/edit/<int:pk>', views.edit_account, name='edit_account'),
    path('accounts/delete/<int:pk>', views.confirm_delete_account, name='delete_account'),
    path('counterparties/', views.table_counterparties, name='counterparties'),
    path('counterparties/edit/<int:pk>', views.edit_counterparty, name='edit_counterparty'),
    path('counterparties/delete/<int:pk>', views.confirm_delete_counterparty, name='delete_counterparty'),
    path('customer_orders/', views.table_customer_orders, name='customer_orders'),
]
