from datetime import datetime, date

from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db import transaction
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from greensite.decorators import prepare_languages

from ledger.models import CustomerOrder
from ledger.forms import CustomerOrderForm, CustomerOrderPositionsFormset, CustomerOrderPositionFormHelper


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


class CustomerOrderCreate(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = CustomerOrder
    form_class = CustomerOrderForm
    success_message = "Customer Order successfully created"
    success_url = reverse_lazy('ledger:customer_orders')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Add Customer Order'
        context['heading'] = 'Ledger'

        if self.request.POST:
            context['positions_formset'] = CustomerOrderPositionsFormset(self.request.POST, instance=self.object)
            context['positions_formset'].full_clean()
            context['positions_helper'] = CustomerOrderPositionFormHelper()
        else:
            context['positions_formset'] = CustomerOrderPositionsFormset(instance=self.object)
            context['positions_helper'] = CustomerOrderPositionFormHelper()

        return context

    def get_initial(self):
        initial = super().get_initial()
        initial = initial.copy()
        initial['DateOperation'] = date.today()
        return initial

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def form_valid(self, form):
        context=self.get_context_data()
        positions_formset = context['positions_formset']

        form.instance.User = self.request.user
        return super().form_valid(form)


class CustomerOrderUpdate(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = CustomerOrder
    form_class = CustomerOrderForm
    success_message = "Customer Order successfully updated"
    success_url = reverse_lazy('ledger:customer_orders')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edit Customer Order'
        context['heading'] = 'Ledger'

        if self.request.POST:
            context['positions_formset'] = CustomerOrderPositionsFormset(self.request.POST, instance=self.object)
            context['positions_formset'].full_clean()
            context['positions_helper'] = CustomerOrderPositionFormHelper()
        else:
            context['positions_formset'] = CustomerOrderPositionsFormset(instance=self.object)
            context['positions_helper'] = CustomerOrderPositionFormHelper()

        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def form_valid(self, form):
        context=self.get_context_data()
        positions_formset = context['positions_formset']

        if not form.has_changed() and not positions_formset.has_changed():
            form.add_error(None, 'Order data and positions were not changed')
            return super().form_invalid(form)

        if form.is_valid() and positions_formset.is_valid():
            with transaction.atomic():
                if form.has_changed():
                    self.object = form.save(commit=False)
                    # We don't need to set User because this class is Update, not Create
                    self.object.save()

                if positions_formset.has_changed():
                    positions_objects = positions_formset.save(commit=False)
                    for position in positions_objects:
                        # We don't need to set Operation here because InlineFormset already handled this
                        position.save()
                    for position in positions_formset.deleted_objects:
                        # We can check for something here
                        position.delete()

        return super(SuccessMessageMixin, self).form_valid(form)


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
