from datetime import datetime, date
from itertools import groupby
from operator import itemgetter

from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Value, F, DecimalField, Case, When, Q, FilteredRelation
from django.template.response import TemplateResponse

from django_tables2 import RequestConfig

from greensite.decorators import prepare_languages
from products.models import Product

from ledger.models import CustomerOrderPosition, SupplierOrderPosition, ItemSetBreakdownPosition,\
    Payment, Transfer, DEBIT, CREDIT
from ledger.tables import InStockTable, FundsTable


@login_required
@prepare_languages
def view_stock(request):
    date_report = datetime.strptime(request.GET.get("reportDate", date.today().strftime("%Y-%m-%d")), "%Y-%m-%d").date()

    dict_customer_orders = {pos.get('Product__SKU'): pos for pos in CustomerOrderPosition.objects \
        .values('Product__SKU') \
        .annotate(
            delivered=Sum(Case(
                When(Q(DateDelivered__lte=date_report),
                     Operation__DateOperation__lte=date_report,
                     then=F('Quantity')),
                default=0)),
            not_delivered=Sum(Case(
                When((Q(DateDelivered__isnull=True) | Q(DateDelivered__gt=date_report)),
                     Operation__DateOperation__lte=date_report,
                     then=F('Quantity')),
                default=0)),
            not_delivered_4=Sum(Case(
                When((Q(DateDelivered__isnull=True) | Q(DateDelivered__gt=date_report)),
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
        p["reserved"] = 0
        p["available"] = p["in_stock"] + p["supp_not_delivered"] - p["cust_not_delivered"] - p["reserved"]

    list_in_stock = [i for i in list_in_stock
                     if (i["in_stock"] != 0) | (i["supp_not_delivered"] != 0) | (i["cust_not_delivered"] != 0)]

    return TemplateResponse(request, 'ledger/ecommerce-warehouse.html', {
        'title': 'Warehouse',
        'heading': 'Ledger',
        'table': list_in_stock,
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
