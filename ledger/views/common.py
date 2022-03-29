from datetime import datetime, date

from django.contrib.auth.decorators import login_required, permission_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.utils.translation import gettext_lazy as _

from greensite.decorators import prepare_languages

from ledger.models import CustomerOrder, CustomerOrderPosition, Payment, CREDIT
from ledger.tables import CustomerOrderPositionsTable, CustomerOrderPaymentsTable
from ledger.forms import CustomerOrderPositionForm, CustomerOrderPaymentForm
from ledger.classes import CrudActionView, CrudDeleteView


@login_required
@prepare_languages
def view_index(request):
    return TemplateResponse(request, 'ledger/index.html')


@login_required
@permission_required('ledger.view_customerorderposition', raise_exception=True)
def table_customer_order_positions(request):
    customer_order_instance = get_object_or_404(CustomerOrder, id=request.GET.get('id'), User=request.user)
    table = CustomerOrderPositionsTable(CustomerOrderPosition.objects.filter(Operation=customer_order_instance.id))
    if not customer_order_instance.DetailedDelivery:
        table.exclude = ('DateDelivered', )

    rendered_table = table.as_html(request)
    return JsonResponse({'status': 'success',
                         'table': rendered_table})


class CustomerOrderPositionAction(CrudActionView):
    model = CustomerOrderPosition
    exclude = ['Product', 'operation_ptr', 'User']
    form = CustomerOrderPositionForm
    parent_id_field = 'Operation'
    parent_model = CustomerOrder
    user_id_field = 'Operation__User'
    msg_name_class = _('Position of Customer Order')

    def get_default_info(self, instance):
        # Usually we have only "model"."parent_id_field" and "model".User filled
        params = {}
        if instance.Operation:
            # if we know order id, then we help with calculations
            params['Currency'] = instance.Operation.Currency
        return {**params}

    def get_additional_info(self, instance):
        # Strange thing, direct access to empty instance.Product gives an exception
        return {
            'Product': {'value': instance.Product.pk,
                        'text': f'#{instance.Product.get_full_name()}'
                        } if instance.Product_id else {},
        }


class CustomerOrderPositionDelete(CrudDeleteView):
    model = CustomerOrderPosition
    msg_name_class = _('Position of Customer Order')


@login_required
@permission_required('ledger.view_payment', raise_exception=True)
def table_customer_order_payments(request):
    customer_order_instance = get_object_or_404(CustomerOrder, id=request.GET.get('id'), User=request.user)
    table = CustomerOrderPaymentsTable(Payment.objects.filter(ParentOperation=customer_order_instance.id))

    rendered_table = table.as_html(request)
    return JsonResponse({'status': 'success',
                         'table': rendered_table})


class CustomerOrderPaymentAction(CrudActionView):
    model = Payment
    exclude = ['operation_ptr', 'User']
    form = CustomerOrderPaymentForm
    parent_id_field = 'ParentOperation'
    parent_model = CustomerOrder
    msg_name_class = _('Payment of Customer Order')

    def get_default_info(self, instance):
        # Usually we have only "model"."parent_id_field" and "model".User filled
        params = {'DateOperation': date.today(), 'TransactionType': CREDIT}
        if instance.ParentOperation:
            # if we know order id, then we help with calculations
            params['Amount'] = instance.ParentOperation.Amount - instance.ParentOperation.get_paid_amount
            params['Currency'] = instance.ParentOperation.Currency
        return {**params}


class CustomerOrderPaymentDelete(CrudDeleteView):
    model = Payment
    msg_name_class = _('Payment of Customer Order')


@login_required
def database_validation(request):
    # При вызове через POST мы выполняем первый блок (статистика), дальнейшие блоки вызываются уже по очереди через AJAX
    # и таким образом формируют лог проверки
    # 1. SupplierOrder
    #   1a. Сумма ордера равна сумме позиций с ценой без отметки GiftPosition и FreeOnAction плюс доставка
# Нужен контроль за полем Status в SupplierOrderPosition:
# 1. Для доставленных заказов (DateDelivery в заказе или позиции) должен быть статус 6 (Delivered)
# 2.
#
# Для полностью закрытых заказов с частичной поставкой дата закрытия всего заказа ставится по последней дате

    if request.POST():
        pass
