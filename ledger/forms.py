from django.forms import ModelForm, DateInput
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Div, Field, Layout, HTML, Row
from crispy_forms.bootstrap import PrependedText

from .models import Account, Counterparty, CustomerOrder, CustomerOrderPosition, Payment


class AccountForm(ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user') if 'user' in kwargs else None # notice the .pop()
        super().__init__(*args, **kwargs)

        # Remove help_text to make it as tooltips
        for field_name, field in self.fields.items():
            self.fields[field_name].help_text = None

        self.helper = FormHelper()
        self.helper.layout = Layout(
            PrependedText('Name', mark_safe('<i class="uil-university"></i>'), autocomplete="off"),
        )

        # loading Model descriptors from Meta subclass
        for fld in self._meta.model._meta.get_fields():
            if not fld.auto_created:
                self.helper[fld.name].update_attributes(placeholder=fld.verbose_name)
                if fld.help_text != '':
                    self.helper[fld.name].update_attributes(title=fld.help_text)
                    self.helper[fld.name].update_attributes(data_bs_toggle="tooltip")

        self.helper.form_show_labels = False
        self.helper.use_custom_control = True
        self.helper.form_tag = False
        self.helper.disable_csrf = True

    class Meta:
        model = Account
        fields = ['Name', ]


class CounterpartyForm(ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user') if 'user' in kwargs else None # notice the .pop()
        super().__init__(*args, **kwargs)

        # Remove help_text to make it as tooltips
        for field_name, field in self.fields.items():
            self.fields[field_name].help_text = None

        self.helper = FormHelper()
        self.helper.layout = Layout(
            PrependedText('Name', mark_safe('<i class="uil-user-circle"></i>')),
            Row(
                PrependedText('Phone', mark_safe('<i class="uil-phone"></i>'), wrapper_class='col-md-4'),
                PrependedText('Email', mark_safe('<i class="uil-envelope"></i>'), wrapper_class='col-md-4'),
                PrependedText('Telegram', mark_safe('<i class="uil-telegram-alt"></i>'), wrapper_class='col-md-4'),
            ),
            Row(
                PrependedText('Instagram', mark_safe('<i class="uil-instagram"></i>'), wrapper_class='col-md-4'),
                PrependedText('Facebook', mark_safe('<i class="uil-facebook-messenger"></i>'), wrapper_class='col-md-4'),
                PrependedText('City', mark_safe('<i class="uil-building"></i>'), wrapper_class='col-md-4'),
            ),
            PrependedText('Address', mark_safe('<i class="uil-sign-alt"></i>')),
            Field('Memo', rows=4),
            HTML('<label>A Customer may act as a Supplier or Customer, or both</label>'),
            Row(
                Field('IsSupplier', template='ledger/crispy_custom_checkbox.html', wrapper_class='col-md-6'),
                Field('IsCustomer', template='ledger/crispy_custom_checkbox.html', wrapper_class='col-md-6'),
            ),
        )

        # loading Model descriptors from Meta subclass
        for fld in self._meta.model._meta.get_fields():
            if not fld.auto_created:
                self.helper[fld.name].update_attributes(placeholder=fld.verbose_name)
                if fld.help_text != '':
                    self.helper[fld.name].update_attributes(title=fld.help_text)
                    self.helper[fld.name].update_attributes(data_bs_toggle="tooltip")

        self.helper.form_show_labels = False
        self.helper.use_custom_control = True
        self.helper.form_tag = False
        self.helper.disable_csrf = True

    def clean(self):
        data = super().clean()
        if data['IsCustomer'] == False and data['IsSupplier'] == False:
            self.add_error(None, 'A Counterparty should be a Customer or Supplier, or both')
        return data

    class Meta:
        model = Counterparty
        fields = ['Name', 'Phone', 'Email', 'Telegram', 'Instagram', 'Facebook', 'Address', 'City', 'Memo',
                  'IsSupplier', 'IsCustomer', ]


class CustomerOrderForm(ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user') if 'user' in kwargs else None # notice the .pop()
        super().__init__(*args, **kwargs)

        # Remove help_text to make it as tooltips
        for field_name, field in self.fields.items():
            self.fields[field_name].help_text = None

        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                PrependedText('DateOperation', mark_safe('<i class="uil-calendar-alt"></i>'), wrapper_class='col-md-4'),
                Field('Customer',
                      css_class='select2',
                      wrapper_class='col-md-8'),
            ),
            Row(
                PrependedText('DateDispatched', mark_safe('<i class="uil-truck"></i>'), wrapper_class='col-md-4'),
                PrependedText('TrackingNumber', mark_safe('<i class="uil-bug"></i>'), wrapper_class='col-md-4'),
                PrependedText('CourierService', mark_safe('<i class="uil-post-stamp"></i>'), wrapper_class='col-md-4'),
            ),
            Row(
                PrependedText('DateDelivered', mark_safe('<i class="uil-gift"></i>'), wrapper_class='col-md-6'),
                Field('DetailedDelivery', template='ledger/crispy_custom_checkbox.html', wrapper_class='col-md-6'),
            ),
            Row(
                PrependedText('Amount', mark_safe('<i class="bi bi-cash-stack"></i>'), wrapper_class='col-md-4',
                              css_class="text-right"),
                Field('Currency', wrapper_class='col-md-4'),
            ),
            Field('Memo', rows=4),
        )

        # queryset_filters = dict(User=self.user)
        external_instance = kwargs['instance']
        if external_instance:
            queryset_filters = dict(pk=external_instance.Customer.pk)
            self.fields['Customer'].queryset = Counterparty.objects.filter(
                **{k: v for k, v in queryset_filters.items() if v is not None}
            )

        # loading Model descriptors from Meta subclass
        for fld in self._meta.model._meta.get_fields():
            if not fld.auto_created:
                self.helper[fld.name].update_attributes(placeholder=fld.verbose_name)
                if fld.help_text:
                    self.helper[fld.name].update_attributes(title=fld.help_text)
                    self.helper[fld.name].update_attributes(data_bs_toggle="tooltip")

        self.helper.form_show_labels = False
        self.helper.use_custom_control = True
        self.helper.form_tag = False
        self.helper.disable_csrf = True

    class Meta:
        model = CustomerOrder
        fields = ['DateOperation', 'Customer', 'DateDispatched', 'DateDelivered', 'TrackingNumber',
                  'CourierService', 'DetailedDelivery', 'Amount', 'Currency', 'Memo', ]


class CustomerOrderPositionForm(ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user') if 'user' in kwargs else None # notice the .pop()
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            self.fields[field_name].help_text = None

        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('Product',
                  css_class='basicAutoSelect',
                  autocomplete='off',
                  data_url=reverse('ledger:product_search')),
            Div(
                PrependedText('Quantity', '<i class="bi bi-123"></i>', wrapper_class='col-md-4',
                              css_class="text-right"),
                PrependedText('Price', '<i class="bi bi-cash-stack"></i>', wrapper_class='col-md-4',
                              css_class="text-right"),
                PrependedText('Currency', '<i class="bi bi-currency-exchange"></i>', wrapper_class='col-md-4'),
                css_class='form-row'),
            Div(
                PrependedText('Discount', '<i class="bi bi-piggy-bank"></i>', wrapper_class='col-md-4',
                              css_class="text-right"),
                Field('DiscountReason', wrapper_class='col-md-8'),
                css_class='form-row'),
            PrependedText('Status', '<i class="bi bi-basket"></i>'),
            PrependedText('DateDelivered', '<i class="bi bi-gift"></i>')
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

        self.prefix = 'form_CustomerOrderPosition'

    class Meta:
        model = CustomerOrderPosition
        fields = ['Product', 'Quantity', 'Price', 'Currency', 'Discount', 'DiscountReason', 'Status', 'DateDelivered']


class CustomerOrderPaymentForm(ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user') if 'user' in kwargs else None # notice the .pop()
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            self.fields[field_name].help_text = None

        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                PrependedText('DateOperation', '<i class="bi bi-calendar-date"></i>', wrapper_class='col-md-6'),
                Field('TransactionType', wrapper_class='col-md-6'),
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

        self.prefix = 'form_CustomerOrderPayment'

    class Meta:
        model = Payment
        fields = ['DateOperation', 'TransactionType', 'Account', 'Amount', 'Currency', ]
