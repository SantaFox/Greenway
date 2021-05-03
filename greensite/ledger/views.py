from datetime import datetime

from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.db.models import OuterRef, Sum, Subquery, Value, DecimalField
from django.db.models.functions import Coalesce,Cast
from django.shortcuts import get_object_or_404
from django.http import JsonResponse, Http404, HttpResponseBadRequest
from django.template.response import TemplateResponse
from django.forms.models import model_to_dict

from django_tables2 import RequestConfig

from greensite.decorators import prepare_languages

from .models import Account, Counterparty, CustomerOrder, CustomerOrderPosition, Payment
from .tables import AccountsTable, CounterpartyTable, CustomerOrdersTable, CustomerOrderPositionsTable
from .forms import AccountForm, CounterpartyForm, CustomerOrderForm
from .filters import CustomerOrderFilter


@login_required
@prepare_languages
def view_index(request):
    return TemplateResponse(request, 'ledger/index.html')


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
        'form': form,
    })


def counterparty_action(request):
    if request.is_ajax():
        if request.method == 'GET':
            request_id = request.GET.get('id')
            counterparty_instance = get_object_or_404(Counterparty, id=request_id)
            # TODO: Maybe it's better to create and serialize a CounterpartyForm here?
            counterparty_dict = model_to_dict(counterparty_instance,
                                              fields=['id', 'Name', 'Phone', 'Email', 'Instagram', 'Telegram',
                                                      'Facebook', 'City', 'Address', 'Memo',
                                                      'IsSupplier', 'IsCustomer', ])
            return JsonResponse(counterparty_dict)
        elif request.method == 'POST':
            action = request.POST.get('action')
            if action == 'add':
                counterparty_form = CounterpartyForm(request.POST)
                if not counterparty_form.is_valid():
                    return JsonResponse({'status': 'not_valid',
                                         'message': {
                                             'text': f'Counterparty <strong>{counterparty_form.cleaned_data["Name"]}</strong> was not saved',
                                             'moment': datetime.now(),
                                         },
                                         'errors': counterparty_form.errors})
                counterparty_instance = counterparty_form.save(commit=False)
                counterparty_instance.User = request.user
                try:
                    counterparty_instance.save()
                    messages.success(request,
                                     f'Counterparty <strong>{counterparty_instance.Name}</strong> added successfully')
                    return JsonResponse({'status': 'success'})
                except IntegrityError as e:
                    return JsonResponse({'status': 'not_valid',
                                         'message': {
                                             'text': f'Counterparty <strong>{counterparty_instance.Name}</strong> was not saved',
                                             'moment': datetime.now(),
                                         },
                                         'errors': e.args
                                         })
            elif action == 'edit':
                request_id = request.POST.get('id')
                counterparty_instance = get_object_or_404(Counterparty, id=request_id)
                counterparty_form = CounterpartyForm(request.POST, instance=counterparty_instance)
                if not counterparty_form.has_changed():
                    messages.info(request,
                                  f'Counterparty <strong>{counterparty_instance.Name}</strong> was not changed')
                    return JsonResponse({'status': 'not_changed'})
                if not counterparty_form.is_valid():
                    return JsonResponse({'status': 'not_valid',
                                         'message': {
                                             'text': f'Counterparty <strong>{counterparty_instance.Name}</strong> was not saved',
                                             'moment': datetime.now(),
                                         },
                                         'errors': counterparty_form.errors})
                counterparty_form.save()
                messages.success(request,
                                 f'Counterparty <strong>{counterparty_instance.Name}</strong> updated successfully')
                return JsonResponse({'status': 'success'})
            else:
                return HttpResponseBadRequest()
        else:
            raise Http404
    else:
        raise Http404


def counterparty_delete(request):
    if request.is_ajax():
        if request.method == 'GET':
            request_id = request.GET.get('id')
            counterparty_instance = get_object_or_404(Counterparty, id=request_id)
            related = counterparty_instance.is_deletable()
            related_dict = {str(rel.model._meta.verbose_name_plural): list(i.__str__() for i in rel.all()) for rel in
                            related}
            if related:
                return JsonResponse({'status': 'related_found',
                                     'related': related_dict})
            else:
                return JsonResponse({'status': 'ok'})
        elif request.method == 'POST':
            request_id = request.POST.get('id')
            counterparty_instance = get_object_or_404(Counterparty, id=request_id)
            try:
                counterparty_instance.delete()
                messages.success(request,
                                 f'Counterparty <strong>{counterparty_instance.Name}</strong> deleted successfully')
                return JsonResponse({'status': 'success'})
            except:
                print('Error on deletion')
                return JsonResponse({'status': 'not_valid',
                                     # 'message': {
                                     #     'text': f'Counterparty <strong>{counterparty_instance.Name}</strong> was not saved',
                                     #     'moment': datetime.now(),
                                     # },
                                     # 'errors': counterparty_form.errors
                                     })
        else:
            raise Http404
    else:
        raise Http404


@login_required
@permission_required('ledger.view_account', raise_exception=True)
@prepare_languages
def table_accounts(request):
    table = AccountsTable(Account.objects.filter(User=request.user))
    RequestConfig(request).configure(table)

    return TemplateResponse(request, 'ledger/table_accounts.html', {
        'table': table,
    })


def account_action(request):
    if request.is_ajax():
        if request.method == 'GET':
            request_id = request.GET.get('id')
            account_instance = get_object_or_404(Account, id=request_id)
            # TODO: Maybe it's better to create and serialize a CounterpartyForm here?
            counterparty_dict = model_to_dict(account_instance,
                                              fields=['id', 'Name', ])
            return JsonResponse(counterparty_dict)
        elif request.method == 'POST':
            action = request.POST.get('action')
            if action == 'add':
                account_form = AccountForm(request.POST)
                if not account_form.is_valid():
                    return JsonResponse({'status': 'not_valid',
                                         'message': {
                                             'text': f'Account <strong>{account_form.cleaned_data["Name"]}</strong> was not saved',
                                             'moment': datetime.now(),
                                         },
                                         'errors': account_form.errors})
                account_instance = account_form.save(commit=False)
                account_instance.User = request.user
                try:
                    account_instance.save()
                    messages.success(request,
                                     f'Account <strong>{account_instance.Name}</strong> added successfully')
                    return JsonResponse({'status': 'success'})
                except IntegrityError as e:
                    return JsonResponse({'status': 'not_valid',
                                         'message': {
                                             'text': f'Counterparty <strong>{account_instance.Name}</strong> was not saved',
                                             'moment': datetime.now(),
                                         },
                                         'errors': e.args
                                         })
            elif action == 'edit':
                request_id = request.POST.get('id')
                account_instance = get_object_or_404(Account, id=request_id)
                account_form = CounterpartyForm(request.POST, instance=account_instance)
                if not account_form.has_changed():
                    messages.info(request,
                                  f'Account <strong>{account_instance.Name}</strong> was not changed')
                    return JsonResponse({'status': 'not_changed'})
                if not account_form.is_valid():
                    return JsonResponse({'status': 'not_valid',
                                         'message': {
                                             'text': f'Account <strong>{account_instance.Name}</strong> was not saved',
                                             'moment': datetime.now(),
                                         },
                                         'errors': account_form.errors})
                account_form.save()
                messages.success(request,
                                 f'Account <strong>{account_instance.Name}</strong> updated successfully')
                return JsonResponse({'status': 'success'})
            else:
                return HttpResponseBadRequest()
        else:
            raise Http404
    else:
        raise Http404


def account_delete(request):
    if request.is_ajax():
        if request.method == 'GET':
            request_id = request.GET.get('id')
            account_instance = get_object_or_404(Account, id=request_id)
            related = account_instance.is_deletable()
            related_dict = {str(rel.model._meta.verbose_name_plural): list(i.__str__() for i in rel.all()) for rel in
                            related}
            if related:
                return JsonResponse({'status': 'related_found',
                                     'related': related_dict})
            else:
                return JsonResponse({'status': 'ok'})
        elif request.method == 'POST':
            request_id = request.POST.get('id')
            account_instance = get_object_or_404(Account, id=request_id)
            try:
                account_instance.delete()
                messages.success(request,
                                 f'Account <strong>{account_instance.Name}</strong> deleted successfully')
                return JsonResponse({'status': 'success'})
            except:
                print('Error on deletion')
                return JsonResponse({'status': 'not_valid',
                                     # 'message': {
                                     #     'text': f'Counterparty <strong>{counterparty_instance.Name}</strong> was not saved',
                                     #     'moment': datetime.now(),
                                     # },
                                     # 'errors': counterparty_form.errors
                                     })
        else:
            raise Http404
    else:
        raise Http404


@login_required
@permission_required('ledger.view_customerorder', raise_exception=True)
@prepare_languages
def table_customer_orders(request):
    # comments = Comment.objects.filter(post=OuterRef('pk')).order_by().values('post')
    # >> > total_comments = comments.annotate(total=Sum('length')).values('total')
    # >> > Post.objects.filter(length__gt=Subquery(total_comments))

    subq = Payment.objects.filter(ParentOperation=OuterRef('pk')).values('ParentOperation')
    sum_paid = subq.annotate(total=Sum('Amount')).values('total')

    qst = CustomerOrder.objects.filter(User=request.user).exclude(Amount=Coalesce(Subquery(sum_paid), Value(0)))

    f = CustomerOrderFilter(request.GET, queryset=qst)
    table = CustomerOrdersTable(f.qs)
    RequestConfig(request,
                  paginate={"per_page": 15}) \
        .configure(table)

    form = CustomerOrderForm()
    return TemplateResponse(request, 'ledger/table_customer_orders.html', {
        'table': table,
        'form': form,
    })


def customer_order_action(request):
    if request.is_ajax():
        if request.method == 'GET':
            request_id = request.GET.get('id')
            item_instance = get_object_or_404(CustomerOrder, id=request_id)
            # TODO: Maybe it's better to create and serialize a CounterpartyForm here?
            # item_form = CustomerOrderForm(instance=item_instance)
            item_dict = model_to_dict(item_instance, exclude=('operation_ptr', 'User', 'Type'))
            item_dict['positions_count'] = item_instance.positions_count
            item_dict['payments_count'] = item_instance.payments_count
            return JsonResponse(item_dict)
        elif request.method == 'POST':
            action = request.POST.get('action')
            if action == 'add':
                item_form = CustomerOrderForm(request.POST)
                if not item_form.is_valid():
                    return JsonResponse({'status': 'not_valid',
                                         'message': {
                                             'text': f'Customer Order <strong>{item_form.cleaned_data["Name"]}</strong> was not saved',
                                             'moment': datetime.now(),
                                         },
                                         'errors': item_form.errors})
                item_instance = item_form.save(commit=False)
                item_instance.User = request.user
                try:
                    item_instance.save()
                    messages.success(request,
                                     f'Customer Order <strong>{item_instance.Name}</strong> added successfully')
                    return JsonResponse({'status': 'success'})
                except IntegrityError as e:
                    return JsonResponse({'status': 'not_valid',
                                         'message': {
                                             'text': f'Customer Order <strong>{item_instance.Name}</strong> was not saved',
                                             'moment': datetime.now(),
                                         },
                                         'errors': e.args
                                         })
            elif action == 'edit':
                request_id = request.POST.get('id')
                item_instance = get_object_or_404(Account, id=request_id)
                item_form = CustomerOrderForm(request.POST, instance=item_instance)
                if not item_form.has_changed():
                    messages.info(request,
                                  f'Customer Order <strong>{item_instance.Name}</strong> was not changed')
                    return JsonResponse({'status': 'not_changed'})
                if not item_form.is_valid():
                    return JsonResponse({'status': 'not_valid',
                                         'message': {
                                             'text': f'Customer Order <strong>{item_instance.Name}</strong> was not saved',
                                             'moment': datetime.now(),
                                         },
                                         'errors': item_form.errors})
                item_form.save()
                messages.success(request,
                                 f'Customer Order <strong>{item_instance.Name}</strong> updated successfully')
                return JsonResponse({'status': 'success'})
            else:
                return HttpResponseBadRequest()
        else:
            raise Http404
    else:
        raise Http404


def customer_order_delete(request):
    if request.is_ajax():
        if request.method == 'GET':
            request_id = request.GET.get('id')
            order_instance = get_object_or_404(CustomerOrder, id=request_id)
            related = order_instance.is_deletable()
            related_dict = {str(rel.model._meta.verbose_name_plural): list(i.__str__() for i in rel.all()) for rel in
                            related}
            if related:
                return JsonResponse({'status': 'related_found',
                                     'related': related_dict}, safe=False)
            else:
                return JsonResponse({'status': 'ok'})
        elif request.method == 'POST':
            request_id = request.POST.get('id')
            order_instance = get_object_or_404(CustomerOrder, id=request_id)
            try:
                order_instance.delete()
                messages.success(request,
                                 f'Customer Order <strong>{order_instance.Name}</strong> deleted successfully')
                return JsonResponse({'status': 'success'})
            except:
                print('Error on deletion')
                return JsonResponse({'status': 'not_valid',
                                     # 'message': {
                                     #     'text': f'Counterparty <strong>{counterparty_instance.Name}</strong> was not saved',
                                     #     'moment': datetime.now(),
                                     # },
                                     # 'errors': counterparty_form.errors
                                     })
        else:
            raise Http404
    else:
        raise Http404


@login_required
@permission_required('ledger.view_customerorderposition', raise_exception=True)
def table_customer_order_positions(request):
    customer_order_instance = get_object_or_404(CustomerOrder, id=request.GET.get('id'), User=request.user)
    table = CustomerOrderPositionsTable(CustomerOrderPosition.objects.filter(Operation=customer_order_instance.id))
    # RequestConfig(request,
    #               paginate={"per_page": 15}) \
    #     .configure(table)

    rendered_table = table.as_html(request)
    return JsonResponse({'status': 'ok',
                         'table': rendered_table})

# TODO: ALL DIRECT REQUESTS SHOULD ALSO CHECK FOR CORRECT USER!!!!!