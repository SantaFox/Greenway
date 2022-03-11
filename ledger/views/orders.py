from datetime import datetime, date

from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.template.response import TemplateResponse
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic.detail import DetailView
from django.views.generic.edit import DeleteView
from extra_views import CreateWithInlinesView, UpdateWithInlinesView, InlineFormSetFactory, SuccessMessageMixin

from greensite.decorators import prepare_languages

from ledger.models import CustomerOrder, CustomerOrderPosition
from ledger.forms import CustomerOrderForm, CustomerOrderPositionForm, CustomerOrderPositionFormHelper


@login_required
@permission_required('ledger.view_customerorder', raise_exception=True)
@prepare_languages
def table_customer_orders(request):
    qst = CustomerOrder.objects.filter(User=request.user)

    return TemplateResponse(request, 'ledger/ecommerce-orders.html', {
        'title': 'Customer Orders',
        'heading': 'Ledger',
        'orders': qst,
    })


class CustomerOrderPositionInline(InlineFormSetFactory):
    model = CustomerOrderPosition
    form_class = CustomerOrderPositionForm
    factory_kwargs = {'extra': 1, 'max_num': None, 'can_order': False, 'can_delete': True}


class CustomerOrderCreate(SuccessMessageMixin, LoginRequiredMixin, CreateWithInlinesView):
    model = CustomerOrder
    form_class = CustomerOrderForm
    inlines = [CustomerOrderPositionInline, ]
    success_message = "Customer Order successfully created"
    success_url = reverse_lazy('ledger:customer_orders')
    extra_context = {'title': 'Add Customer Order',
                     'heading': 'Ledger',
                     'positions_helper': CustomerOrderPositionFormHelper,
                     }

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'user': self.request.user})  # We have a user-related filtering in the form
        return kwargs

    def form_valid(self, form):
        # We update prepared (.save(commit=False)) form's instance with data not expected to be available in form itself
        form.instance.User = self.request.user
        return super().form_valid(form)

    def get_initial(self):
        initial = super().get_initial()
        initial = initial.copy()
        initial['DateOperation'] = date.today()
        return initial


class CustomerOrderUpdate(SuccessMessageMixin, LoginRequiredMixin, UpdateWithInlinesView):
    model = CustomerOrder
    form_class = CustomerOrderForm
    inlines = [CustomerOrderPositionInline, ]
    success_message = "Customer Order successfully updated"
    success_url = reverse_lazy('ledger:customer_orders')
    factory_kwargs = {'extra': 1, 'max_num': None, 'can_order': False, 'can_delete': True}
    extra_context = {'title': 'Edit Customer Order',
                     'heading': 'Ledger',
                     'positions_helper': CustomerOrderPositionFormHelper,
                     }

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'user': self.request.user})  # We have a user-related filtering in the form
        return kwargs


class CustomerOrderDelete(SuccessMessageMixin, LoginRequiredMixin, DeleteView):
    model = CustomerOrder
    success_message = "Customer Order successfully deleted"
    success_url = reverse_lazy('ledger:accounts')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Delete Customer Order'
        context['heading'] = 'Ledger'

        object_instance = self.get_object()
        related = object_instance.is_deletable()
        if related:
            related_dict = {
                str(rel.model._meta.verbose_name_plural): list(i.__str__() for i in rel.all()) for rel in related
            }
            context['related'] = related_dict

        return context


class CustomerOrderPrint(LoginRequiredMixin, DetailView):
    model = CustomerOrder

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Print Customer Order'
        context['heading'] = 'Ledger'

        return context
