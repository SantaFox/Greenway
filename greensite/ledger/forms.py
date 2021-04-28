from django.forms import ModelForm, ModelMultipleChoiceField, CheckboxSelectMultiple, inlineformset_factory
from django.utils.translation import gettext_lazy as _

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Div, Field, Layout

from .models import Counterparty, Account


class CounterpartyForm(ModelForm):
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.helper = FormHelper()
    #     self.helper.layout = Layout(
    #         Div(
    #             Field('Category', wrapper_class='col-md-4'),
    #             Field('DateAdded', wrapper_class='col-md-4'),
    #             Field('DateRemoved', wrapper_class='col-md-4'),
    #             css_class='form-row')
    #     )
    #     self.helper.form_tag = False        # We will use a common form
    #     self.helper.disable_csrf = True

    class Meta:
        model = Counterparty
        fields = ['Name', 'Phone', 'Email', 'Telegram', 'Instagram', 'Facebook', 'Address', 'City', 'Memo',
                  'IsSupplier', 'IsCustomer', ]


class AccountForm(ModelForm):
    class Meta:
        model = Account
        fields = ['Name', ]
