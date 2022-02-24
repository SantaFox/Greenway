from datetime import datetime, date
from itertools import groupby
from operator import itemgetter

from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import OuterRef, Sum, Subquery, Value, Func, F, DecimalField, Case, When, Q, FilteredRelation
from django.db.models.functions import Coalesce, Cast
from django.http import JsonResponse, Http404, HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from django_tables2 import RequestConfig
from crispy_forms.utils import render_crispy_form

from greensite.decorators import prepare_languages
from products.models import Product

from .models import Account, Counterparty, Operation, CustomerOrder, CustomerOrderPosition, SupplierOrderPosition, \
    ItemSetBreakdownPosition, Payment, Transfer, DEBIT, CREDIT
from .tables import InStockTable, FundsTable, AccountsTable, CounterpartyTable, CustomerOrdersTable, \
    CustomerOrderPositionsTable, CustomerOrderPaymentsTable
from .forms import AccountForm, CounterpartyForm, CustomerOrderForm, CustomerOrderPositionForm, CustomerOrderPaymentForm
from .filters import CustomerOrderFilter
from .classes import CrudActionView, CrudDeleteView


@login_required
@prepare_languages
def view_index(request):
    return TemplateResponse(request, 'ledger/index.html')


@login_required
@prepare_languages
def view_stock(request):
    date_report = datetime.strptime(request.GET.get("reportDate", date.today().strftime("%Y-%m-%d")), "%Y-%m-%d").date()

    dict_customer_orders = {pos.get('Product__SKU'): pos for pos in CustomerOrderPosition.objects \
        .values('Product__SKU') \
        .annotate(
            delivered=Sum(Case(
                When(Q(Operation__customerorder__DetailedDelivery=True) &
                     Q(DateDelivered__lte=date_report),
                     Operation__DateOperation__lte=date_report,
                     then=F('Quantity')),
                When(Q(Operation__customerorder__DetailedDelivery=False) &
                     Q(Operation__customerorder__DateDelivered__lte=date_report),
                     Operation__DateOperation__lte=date_report,
                     then=F('Quantity')),
                default=0)),
            not_delivered=Sum(Case(
                When(Q(Operation__customerorder__DetailedDelivery=True) &
                     (Q(DateDelivered__isnull=True) | Q(DateDelivered__gt=date_report)),
                     Operation__DateOperation__lte=date_report,
                     then=F('Quantity')),
                When(Q(Operation__customerorder__DetailedDelivery=False) &
                     (Q(Operation__customerorder__DateDelivered__isnull=True) |
                      Q(Operation__customerorder__DateDelivered__gt=date_report)),
                     Operation__DateOperation__lte=date_report,
                     then=F('Quantity')),
                default=0)),
            not_delivered_4=Sum(Case(
                When(Q(Operation__customerorder__DetailedDelivery=True) &
                     (Q(DateDelivered__isnull=True) | Q(DateDelivered__gt=date_report)),
                     Operation__DateOperation__lte=date_report,
                     Status=4,
                     then=F('Quantity')),
                When(Q(Operation__customerorder__DetailedDelivery=False) &
                     (Q(Operation__customerorder__DateDelivered__isnull=True) |
                      Q(Operation__customerorder__DateDelivered__gt=date_report)),
                     Operation__DateOperation__lte=date_report,
                     Status=4,
                     then=F('Quantity')),
                default=0)),
        ).order_by('Product__SKU')}

    dict_supplier_orders = {pos.get('Product__SKU'): pos for pos in SupplierOrderPosition.objects \
        .values('Product__SKU') \
        .annotate(
            delivered=Sum(Case(
                When(Q(Operation__supplierorder__DateDelivered__lte=date_report),
                     Operation__DateOperation__lte=date_report,
                     then=F('Quantity')),
                default=0)),
            not_delivered=Sum(Case(
                When(Q(Operation__supplierorder__DateDelivered__isnull=True) |
                     Q(Operation__supplierorder__DateDelivered__gt=date_report),
                     Operation__DateOperation__lte=date_report,
                     then=F('Quantity')),
                default=0)),
        ).order_by('Product__SKU')}

    dict_breakdowns = {pos.get('Product__SKU'): pos for pos in ItemSetBreakdownPosition.objects \
        .values('Product__SKU') \
        .annotate(
            received=Sum(Case(
                When(TransactionType=CREDIT, Operation__DateOperation__lte=date_report, then=F('Quantity')),
                default=0)),
            removed=Sum(Case(
                When(TransactionType=DEBIT, Operation__DateOperation__lte=date_report, then=F('Quantity')),
                default=0)),
        ).order_by('Product__SKU')}

    query_products = Product.objects \
        .annotate(pi=FilteredRelation('productinfo', condition=Q(productinfo__Language=request.language_instance))) \
        .values('SKU', 'Category__Name', 'pi__Name').order_by('Category__Name', 'SKU') \

    list_total_stock = []
    for p in query_products:
        list_total_stock.append(
            dict(
                product_SKU=p['SKU'],
                product_name=p['pi__Name'],
                product_category=p['Category__Name'],
                cust_delivered=dict_customer_orders.get(p['SKU'], {}).get('delivered') or 0,
                cust_not_delivered=dict_customer_orders.get(p['SKU'], {}).get('not_delivered') or 0,
                cust_not_delivered_4=dict_customer_orders.get(p['SKU'], {}).get('not_delivered_4') or 0,
                supp_delivered=dict_supplier_orders.get(p['SKU'], {}).get('delivered') or 0,
                supp_not_delivered=dict_supplier_orders.get(p['SKU'], {}).get('not_delivered') or 0,
                break_received=dict_breakdowns.get(p['SKU'], {}).get('received') or 0,
                break_removed=dict_breakdowns.get(p['SKU'], {}).get('removed') or 0,
            )
        )
    # Remove rows for products that were never processed
    list_in_stock = [i for i in list_total_stock if
                     i['cust_delivered'] != 0 or i['cust_not_delivered'] != 0 or
                     i['supp_delivered'] != 0 or i['supp_not_delivered'] != 0 or
                     i['break_received'] != 0 or i['break_removed'] != 0]

    # Prepare sum values and filter positions not in stock if requested
    for p in list_in_stock:
        p["in_stock"] = p["supp_delivered"] - p["cust_delivered"] + p['break_received'] - p['break_removed']
    if request.GET.get("collapse", "false") == "true":
        list_in_stock = [i for i in list_in_stock
                         if (i["in_stock"] != 0) | (i["supp_not_delivered"] != 0) | (i["cust_not_delivered"] != 0)]

    table = InStockTable(list_in_stock)

    RequestConfig(request, paginate=False).configure(table)

    return TemplateResponse(request, 'ledger/table_stocks.html', {
        'table': table,
        'reportDate': date_report,
    })


@login_required
@prepare_languages
def view_funds(request):
    date_start = datetime.strptime(request.GET.get("startDate", '2022-01-01'), "%Y-%m-%d").date()
    date_end = datetime.strptime(request.GET.get("endDate", '2022-12-31'), "%Y-%m-%d").date()

    qry_payments = Payment.objects \
        .values(account=F('Account__Name'), currency=F('Currency__Code')) \
        .annotate(
            initial=Sum(Case(
                When(Q(DateOperation__lt=date_start),
                     TransactionType=DEBIT,
                     then=F('Amount') * -1),
                When(Q(DateOperation__lt=date_start),
                     TransactionType=CREDIT,
                     then=F('Amount') * 1),
                output_field=DecimalField(),
                default=0)),
            debited=Sum(Case(
                When(Q(DateOperation__gte=date_start) & Q(DateOperation__lte=date_end),
                     TransactionType=DEBIT,
                     then=F('Amount')),
                output_field=DecimalField(),
                default=0)),
            credited=Sum(Case(
                When(Q(DateOperation__gte=date_start) & Q(DateOperation__lte=date_end),
                     TransactionType=CREDIT,
                     then=F('Amount')),
                output_field=DecimalField(),
                default=0)),
        )

    qry_transfers_debits = Transfer.objects \
        .values(account=F('DebitAccount__Name'), currency=F('DebitCurrency__Code')) \
        .annotate(
            initial=Sum(Case(
                When(Q(DateOperation__lt=date_start),
                     then=F('DebitAmount') * -1),
                output_field=DecimalField(),
                default=0)),
            debited=Sum(Case(
                When(Q(DateOperation__gte=date_start) & Q(DateOperation__lte=date_end),
                     then=F('DebitAmount')),
                output_field=DecimalField(),
                default=0)),
            credited=Value(0),
        ).exclude(DebitAccount__isnull=True)

    qry_transfers_credits = Transfer.objects \
        .values(account=F('CreditAccount__Name'), currency=F('CreditCurrency__Code')) \
        .annotate(
            initial=Sum(Case(
                When(Q(DateOperation__lt=date_start),
                     then=F('CreditAmount')),
                output_field=DecimalField(),
                default=0)),
            debited=Value(0),
            credited=Sum(Case(
                When(Q(DateOperation__gte=date_start) & Q(DateOperation__lte=date_end),
                     then=F('CreditAmount')),
                output_field=DecimalField(),
                default=0)),
        ).exclude(CreditAccount__isnull=True)

    # modified https://stackoverflow.com/questions/21674331/group-by-multiple-keys-and-summarize-average-values-of-a-list-of-dictionaries
    qry_union = qry_payments.union(qry_transfers_debits, qry_transfers_credits)
    grouper = itemgetter('account','currency')
    result = []
    for key, grp in groupby(sorted(qry_union, key=grouper), grouper):
        temp_list = [item for item in grp]
        temp_dict = dict(zip(['account','currency'], key))
        temp_dict['initial'] = sum(item['initial'] for item in temp_list)
        temp_dict['debited'] = sum(item['debited'] for item in temp_list)
        temp_dict['credited'] = sum(item['credited'] for item in temp_list)
        temp_dict['final'] = temp_dict['initial'] - temp_dict['debited'] + temp_dict['credited']
        result.append(temp_dict)

    table = FundsTable(result)

    return TemplateResponse(request, 'ledger/table_cash.html', {
        'table': table,
        'startDate': date_start,
        'endDate': date_end,
    })


@login_required
@permission_required('ledger.view_counterparty', raise_exception=True)
@prepare_languages
def table_counterparties(request):
    table = CounterpartyTable(Counterparty.objects.filter(User=request.user))
    RequestConfig(request,
                  paginate={"per_page": 15}) \
        .configure(table)

    form = CounterpartyForm
    return TemplateResponse(request, 'ledger/table_counterparties.html', {
        'table': table,
        'forms': [
            {
                'FormId': 'editCounterparty',
                'Action': reverse('ledger:counterparty_action'),
                'Header': _('Edit Counterparty'),
                'CrispyForm': form
            }
        ],
        'deleteAction': reverse('ledger:counterparty_delete'),
        'deleteHeader': _('Delete Counterparty'),
    })


def counterparty_search(request):
    qry = Counterparty.objects.filter(User=request.user)
    search = request.GET.get('q', '')
    response_dict = [{"value": cp.pk, "text": cp.Name} for cp in qry.filter(Name__icontains=search)]
    return JsonResponse(response_dict, safe=False)


class CounterpartyAction(CrudActionView):
    model = Counterparty
    fields = ['id', 'Name', 'Phone', 'Email', 'Instagram', 'Telegram',
              'Facebook', 'City', 'Address', 'Memo', 'IsSupplier', 'IsCustomer']
    form = CounterpartyForm
    msg_name_class = _('Counterparty')
    msg_edit_name = lambda self, instance: instance.Name


class CounterpartyDelete(CrudDeleteView):
    model = Counterparty
    msg_name_class = _('Counterparty')


@login_required
@permission_required('ledger.view_account', raise_exception=True)
@prepare_languages
def table_accounts(request):
    table = AccountsTable(Account.objects.filter(User=request.user))
    RequestConfig(request).configure(table)

    form = AccountForm
    return TemplateResponse(request, 'ledger/table_accounts.html', {
        'table': table,
        'forms': [
            {
                'FormId': 'editAccount',
                'Action': reverse('ledger:account_action'),
                'Header': _('Edit Account'),
                'CrispyForm': form
            }
        ],
        'deleteAction': reverse('ledger:account_delete'),
        'deleteHeader': _('Delete Account'),
    })


class AccountAction(CrudActionView):
    model = Account
    fields = ['id', 'Name']
    form = AccountForm
    msg_name_class = _('Account')
    msg_edit_name = lambda self, instance: instance.Name


class AccountDelete(CrudDeleteView):
    model = Account
    msg_name_class = _('Account')


@login_required
@permission_required('ledger.view_customerorder', raise_exception=True)
@prepare_languages
def table_customer_orders(request):
    qst = CustomerOrder.objects.filter(User=request.user)

    return TemplateResponse(request, 'ledger/ecommerce-orders.html', {
        'title': 'Orders',
        'heading': 'Ledger',
        'orders': qst,
    })



class CustomerOrderAction(CrudActionView):
    model = CustomerOrder
    exclude = ['Customer', 'operation_ptr', 'User']
    form = CustomerOrderForm
    msg_name_class = _('Customer Order')

    def get_additional_info(self, instance):
        return {
            'Customer': {'value': instance.Customer.pk,
                         'text': instance.Customer.Name
                         } if instance.Customer_id else {},
            'positions_count': instance.get_positions_count,
            'payments_count': instance.get_payments_count,
        }

    def get_default_info(self, instance):
        # Usually we have only "model"."parent_id_field" and "model".User filled
        params = {'DateOperation': date.today()}
        return {**params}


class CustomerOrderDelete(CrudDeleteView):
    model = CustomerOrder
    msg_name_class = _('Customer Order')


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


def product_search(request):
    qry = Product.objects.all()
    search = request.GET.get('q', '')
    qry_filter = Q(SKU__icontains=search) | Q(Category__Name__icontains=search) | Q(productinfo__Name__icontains=search)
    response_dict = [
        {"value": cp.pk,
         "text": cp.get_full_name()
         } for cp in qry.filter(qry_filter).order_by('SKU').distinct()
    ]
    return JsonResponse(response_dict, safe=False)


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
