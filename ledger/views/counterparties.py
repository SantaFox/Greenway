from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.template.response import TemplateResponse
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from greensite.decorators import prepare_languages

from ledger.models import Counterparty
from ledger.forms import CounterpartyForm


@login_required
@permission_required('ledger.view_counterparty', raise_exception=True)
@prepare_languages
def table_counterparties(request):
    qst = Counterparty.objects.filter(User=request.user)

    return TemplateResponse(request, 'ledger/ecommerce-customers.html', {
        'title': 'Counterparties',
        'heading': 'Ledger',
        'table': qst,
    })


class CounterpartyCreate(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = Counterparty
    form_class = CounterpartyForm
    success_message = "Counterparty %(Name)s successfully created"
    success_url = reverse_lazy('ledger:counterparties')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Add Counterparty'
        context['heading'] = 'Ledger'
        return context

    # def get_initial(self):
    #     initial = super().get_initial()
    #     initial = initial.copy()
    #     initial['User_id'] = self.request.user.pk
    #     return initial

    def form_valid(self, form):
        form.instance.User = self.request.user
        return super().form_valid(form)


class CounterpartyUpdate(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = Counterparty
    form_class = CounterpartyForm
    success_message = "Counterparty %(Name)s successfully updated"
    success_url = reverse_lazy('ledger:counterparties')

    def form_valid(self, form):
        if not form.has_changed():
            form.add_error(None, 'Form data was not changed')
            return super().form_invalid(form)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edit Counterparty'
        context['heading'] = 'Ledger'
        return context


class CounterpartyDelete(SuccessMessageMixin, LoginRequiredMixin, DeleteView):
    model = Counterparty
    success_message = "Counterparty successfully deleted"
    success_url = reverse_lazy('ledger:counterparties')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Delete Counterparty'
        context['heading'] = 'Ledger'

        object_instance = self.get_object()
        related = object_instance.is_deletable()
        if related:
            related_dict = {
                str(rel.model._meta.verbose_name_plural): list(i.__str__() for i in rel.all()) for rel in related
            }
            context['related'] = related_dict

        return context
