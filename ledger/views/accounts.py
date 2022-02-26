from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.template.response import TemplateResponse
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from greensite.decorators import prepare_languages

from ledger.models import Account
from ledger.forms import AccountForm


@login_required
@permission_required('ledger.view_account', raise_exception=True)
@prepare_languages
def table_accounts(request):
    qst = Account.objects.filter(User=request.user)

    return TemplateResponse(request, 'ledger/ecommerce-accounts.html', {
        'title': 'Accounts',
        'heading': 'Ledger',
        'table': qst,
    })


class AccountCreate(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = Account
    form_class = AccountForm
    success_message = "Account %(Name)s successfully created"
    success_url = reverse_lazy('ledger:accounts')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Add Account'
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


class AccountUpdate(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = Account
    form_class = AccountForm
    success_message = "Account %(Name)s successfully updated"
    success_url = reverse_lazy('ledger:accounts')

    def form_valid(self, form):
        if not form.has_changed():
            form.add_error(None, 'Form data was not changed')
            return super().form_invalid(form)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edit Account'
        context['heading'] = 'Ledger'
        return context


class AccountDelete(SuccessMessageMixin, LoginRequiredMixin, DeleteView):
    model = Account
    success_message = "Account successfully deleted"
    success_url = reverse_lazy('ledger:accounts')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Delete Account'
        context['heading'] = 'Ledger'

        object_instance = self.get_object()
        related = object_instance.is_deletable()
        if related:
            related_dict = {
                str(rel.model._meta.verbose_name_plural): list(i.__str__() for i in rel.all()) for rel in related
            }
            context['related'] = related_dict

        return context
