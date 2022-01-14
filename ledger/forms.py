from django.forms import ModelForm, DateInput
from django.utils.translation import gettext_lazy as _

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Div, Field, Layout, HTML
from crispy_forms.bootstrap import PrependedText

from .models import Account, Counterparty, CustomerOrder, Payment


class AccountForm(ModelForm):
    class Meta:
        model = Account
        fields = ['Name', ]


class CounterpartyForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Remove help_text to make it as tooltips
        for field_name, field in self.fields.items():
            self.fields[field_name].help_text = None

        self.helper = FormHelper()
        self.helper.layout = Layout(
            PrependedText('Name', '<i class="bi bi-person"></i>'),
            Div(
                PrependedText('Phone', '<i class="bi bi-telephone-outbound"></i>', wrapper_class='col-md-6'),
                PrependedText('Email', '<i class="bi bi-envelope"></i>', wrapper_class='col-md-6'),
                css_class='form-row'),
            Div(
                PrependedText('Instagram', '<i class="bi bi-instagram"></i>', wrapper_class='col-md-6'),
                PrependedText('Telegram', '<i class="bi bi-telegram"></i>', wrapper_class='col-md-6'),
                css_class='form-row'),
            Div(
                PrependedText('Facebook', '<i class="bi bi-messenger"></i>', wrapper_class='col-md-6'),
                PrependedText('City', '<i class="bi bi-building"></i>', wrapper_class='col-md-6'),
                css_class='form-row'),
            PrependedText('Address', '<i class="bi bi-signpost-split"></i>'),
            Field('Memo', rows=4),
            HTML('<label>A Customer may act as a Supplier or Customer, or both</label>'),
            Div(
                Field('IsSupplier', template='ledger/crispy_custom_checkbox.html', wrapper_class='col-md-6'),
                Field('IsCustomer', template='ledger/crispy_custom_checkbox.html', wrapper_class='col-md-6'),
                css_class='form-row'),
        )

        # loading Model descriptors from Meta subclass
        for fld in self._meta.model._meta.get_fields():
            if not fld.auto_created:
                self.helper[fld.name].update_attributes(placeholder=fld.verbose_name)
                if fld.help_text != '':
                    self.helper[fld.name].update_attributes(title=fld.help_text)
                    self.helper[fld.name].update_attributes(data_toggle="tooltip")

        self.helper.form_show_labels = False
        self.helper.use_custom_control = True
        self.helper.form_tag = False
        self.helper.disable_csrf = True

    class Meta:
        model = Counterparty
        fields = ['Name', 'Phone', 'Email', 'Telegram', 'Instagram', 'Facebook', 'Address', 'City', 'Memo',
                  'IsSupplier', 'IsCustomer', ]


class CustomerOrderForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # self.fields['DateOperation'].widget = DateInput(attrs={
        #     'required': True,
        #     'class': 'date-time-picker',
        #     'data-options': '{"format":"Y-m-d H:i", "timepicker":"true"}'
        # })

        for field_name, field in self.fields.items():
            self.fields[field_name].help_text = None
            if field_name not in ('DetailedDelivery'):
                self.fields[field_name].label = False

        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                PrependedText('DateOperation', '<i class="bi bi-calendar-date"></i>', wrapper_class='col-md-6'),
                css_class='form-row'),
            PrependedText('Customer', '<i class="bi bi-person"></i>'),
            Div(
                PrependedText('DateDelivered', '<i class="bi bi-gift"></i>', wrapper_class='col-md-6'),
                Field('DetailedDelivery', wrapper_class='col-md-6'),
                css_class='form-row'),
            Div(
                PrependedText('DateDispatched', '<i class="bi bi-truck"></i>', wrapper_class='col-md-6'),
                PrependedText('TrackingNumber', '<i class="bi bi-bug"></i>', wrapper_class='col-md-6'),
                css_class='form-row'),
            Field('CourierService'),
            Div(
                PrependedText('Amount', '<i class="bi bi-cash-stack"></i>', wrapper_class='col-md-4',
                              css_class="text-right"),
                Field('Currency', wrapper_class='col-md-4'),
                css_class='form-row'),
            Field('Memo', rows=4),
        )

        # loading Model descriptors from Meta subclass
        for fld in self._meta.model._meta.get_fields():
            if not fld.auto_created:
                self.helper[fld.name].update_attributes(placeholder=fld.verbose_name)
                if fld.help_text:
                    self.helper[fld.name].update_attributes(title=fld.help_text)
                    self.helper[fld.name].update_attributes(data_toggle="tooltip")

        # self.helper.form_show_labels = False
        self.helper.use_custom_control = True
        self.helper.form_tag = False
        self.helper.disable_csrf = True

    class Meta:
        model = CustomerOrder
        fields = ['DateOperation', 'Customer', 'DateDispatched', 'DateDelivered', 'TrackingNumber',
                  'CourierService', 'DetailedDelivery', 'Amount', 'Currency', 'Memo', ]


class CustomerOrderPaymentForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            self.fields[field_name].help_text = None

        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                PrependedText('DateOperation', '<i class="bi bi-calendar-date"></i>', wrapper_class='col-md-6'),
                css_class='form-row'),
            PrependedText('Account', '<i class="bi bi-menu-button"></i>'),
            Div(
                PrependedText('Amount', '<i class="bi bi-cash-stack"></i>', wrapper_class='col-md-4',
                              css_class="text-right"),
                Field('Currency', wrapper_class='col-md-4'),
                css_class='form-row'),
        )

        # loading Model descriptors from Meta subclass
        for fld in self._meta.model._meta.get_fields():
            if not fld.auto_created:
                self.helper[fld.name].update_attributes(placeholder=fld.verbose_name)
                if fld.help_text != '':
                    self.helper[fld.name].update_attributes(title=fld.help_text)
                    self.helper[fld.name].update_attributes(data_toggle="tooltip")

        self.helper.form_show_labels = False
        self.helper.use_custom_control = True
        self.helper.form_tag = False
        self.helper.disable_csrf = True

    class Meta:
        model = Payment
        fields = ['DateOperation', 'Account', 'Amount', 'Currency', ]
