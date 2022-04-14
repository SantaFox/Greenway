from django.core.exceptions import ValidationError
from django.forms import ModelForm, ModelChoiceField, DecimalField
from django.forms.widgets import NumberInput
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Div, Field, Layout, HTML, Row
from crispy_forms.bootstrap import PrependedText, StrictButton

from .models import Account, Counterparty, CustomerOrder, CustomerOrderPosition, Payment
from products.models import Product


class AccountForm(ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user') if 'user' in kwargs else None # notice the .pop()
        super().__init__(*args, **kwargs)

        # Remove help_text to make it as tooltips
        for field_name, field in self.fields.items():
            self.fields[field_name].help_text = None

        self.helper = FormHelper()
        self.helper.layout = Layout(
            PrependedText('Name', mark_safe('<i class="bi bi-cash-coin"></i>'), autocomplete="off"),
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
            PrependedText('Name', mark_safe('<i class="bi bi-person"></i>')),
            Row(
                PrependedText('Phone', mark_safe('<i class="bi bi-telephone-outbound"></i>'), wrapper_class='col-md-4'),
                PrependedText('Email', mark_safe('<i class="bi bi-envelope"></i>'), wrapper_class='col-md-4'),
                PrependedText('Telegram', mark_safe('<i class="bi bi-telegram"></i>'), wrapper_class='col-md-4'),
            ),
            Row(
                PrependedText('Instagram', mark_safe('<i class="bi bi-instagram"></i>'), wrapper_class='col-md-4'),
                PrependedText('Facebook', mark_safe('<i class="bi bi-messenger"></i>'), wrapper_class='col-md-4'),
                PrependedText('City', mark_safe('<i class="bi bi-building"></i>'), wrapper_class='col-md-4'),
            ),
            Row(
                PrependedText('Address', mark_safe('<i class="bi bi-signpost-split"></i>'), wrapper_class='col-md-8'),
                PrependedText('Coordinates', mark_safe('<i class="bi bi-geo"></i>'), wrapper_class='col-md-4')
            ),
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
        fields = ['Name', 'Phone', 'Email', 'Telegram', 'Instagram', 'Facebook', 'Address', 'City', 'Coordinates',
                  'Memo', 'IsSupplier', 'IsCustomer', ]


class CustomerChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.Name


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
                PrependedText('DateOperation', mark_safe('<i class="bi bi-calendar-date"></i>'), wrapper_class='col-md-3'),
                Field('Currency',
                      css_class='select2',
                      data_placeholder=_('Order Currency'),
                      data_minimum_results_for_search='Infinity',
                      wrapper_class='col-md-2'),
                Field('Customer',
                      css_class='select2',
                      data_ajax__url=reverse('ledger:counterparties_search'),
                      data_ajax__cache=True,
                      data_placeholder=_('Customer Name'),
                      wrapper_class='col-md-7'),
            ),
            Row(
                PrependedText('DateDelivered', mark_safe('<i class="bi bi-gift"></i>'), wrapper_class='col-md-3'),
                HTML('<div class="mb-3 col-md-2 d-flex align-items-center justify-content-end">'
                     '<span>' +
                     _('For Postal Delivery, please fill:') +
                     '</span>'
                     '</div>'),
                PrependedText('DateDispatched', mark_safe('<i class="bi bi-truck"></i>'), wrapper_class='col-md-2'),
                PrependedText('TrackingNumber', mark_safe('<i class="bi bi-bug"></i>'), wrapper_class='col-md-2'),
                PrependedText('CourierService', mark_safe('<i class="bi bi-postage-heart"></i>'), wrapper_class='col-md-3'),
            ),
            # Row(
            #     Field('DetailedDelivery', template='ledger/crispy_custom_checkbox.html', wrapper_class='col-md-6'),
            #     # Field('DetailedDelivery', wrapper_class='col-md-4'),
            # ),
            # Row(
            #     PrependedText('Amount', mark_safe('<i class="uil-bill"></i>'), wrapper_class='col-md-4',
            #                   css_class="text-right"),
            # ),
            Field('Memo', rows=3),
        )

        queryset_filters = dict(User=self.user)
        external_instance = kwargs.get('instance', None)
        if external_instance:
            queryset_filters['pk'] = external_instance.Customer.pk

        self.fields['Customer'].queryset = Counterparty.objects.filter(
            **{k: v for k, v in queryset_filters.items() if v is not None}
        )

        # Fields rendered as <select> are cleaned to show placeholders
        self.fields['Customer'].empty_label = ''
        self.fields['CourierService'].empty_label = ''
        self.fields['Currency'].empty_label = ''

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
                  # 'CourierService', 'DetailedDelivery', 'Amount', 'Currency', 'Memo', ]
                  'CourierService', 'Currency', 'Memo', ]
        field_classes = {
            'Customer': CustomerChoiceField,
        }


class ProductChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.get_full_name()

    # We override this validation method to resolve situation when form is posted with updated value
    # which absent in initial queryset; however, as selection works via AJAX, it is allowed
    def to_python(self, value):
        if value in self.empty_values:
            return None
        try:
            key = self.to_field_name or 'pk'
            if isinstance(value, self.queryset.model):
                value = getattr(value, key)
            # value = self.queryset.get(**{key: value})
            value = self.queryset.model.objects.get(**{key: value})
        except (ValueError, TypeError, self.queryset.model.DoesNotExist):
            raise ValidationError(
                self.error_messages['invalid_choice'],
                code='invalid_choice',
                params={'value': value},
            )
        return value


class CustomerOrderPositionForm(ModelForm):
    subtotal = DecimalField(
        decimal_places=2,
        widget=NumberInput
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user') if 'user' in kwargs else None # notice the .pop()
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            self.fields[field_name].help_text = None

        queryset_filters = dict()
        external_instance = kwargs.get('instance', None)
        queryset_filters['pk'] = external_instance.Product.pk if external_instance else 0

        self.fields['Product'].queryset = Product.objects.filter(
            **{k: v for k, v in queryset_filters.items() if v is not None}
        )
        self.fields['Product'].empty_label = ''

        self.fields['subtotal'].initial =\
            (external_instance.Price * external_instance.Quantity) - (external_instance.Discount or 0)\
            if external_instance else None

    class Meta:
        model = CustomerOrderPosition
        fields = ['Product', 'Quantity', 'Price', 'Discount', 'subtotal', 'DiscountReason', 'Status', 'DateDelivered']
        field_classes = {
            'Product': ProductChoiceField,
        }


class CustomerOrderPositionFormHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.layout = Layout(
            Row(
                Field('Product',
                      css_class='select2',
                      data_ajax__url=reverse('ledger:products_search'),
                      data_ajax__cache=True,
                      data_placeholder=_('Product'),
                      data_minimum_input_length=2,
                      data_dropdown_auto_width='true',
                      wrapper_class='col-md-3'),
                Field('Quantity', wrapper_class='col-md-1', css_class='text-end'),
                Field('Price', wrapper_class='col-md-1', css_class='text-end', readonly=True),
                Field('Discount', wrapper_class='col-md-1', css_class='text-end'),
                Field('subtotal', wrapper_class='col-md-1', css_class='text-end', readonly=True),
                Field('DiscountReason', wrapper_class='col-md-2'),
                Field('Status', wrapper_class='col-md-1'),
                Field('DateDelivered', wrapper_class='col-md-1'),
                Field('DELETE', type="hidden"),
                Div(
                    # This DIV is a placeholder for Remove button added by JavaScript
                    css_class='col-md-1 remove-position-placeholder'
                ),
            ),
        )
        # self.render_required_fields = True
        # mark_safe('<i class="uil-calculator-alt"></i>')
        # mark_safe('<i class="uil-pricetag-alt"></i>')
        # mark_safe('<i class="uil-euro"></i>')
        # mark_safe('<i class="uil-percentage"></i>')
        # mark_safe('<i class="uil-puzzle-piece"></i>')
        # mark_safe('<i class="uil-truck-loading"></i>')
        # loading Model descriptors from Meta subclass
        # for fld in self._meta.model._meta.get_fields():
        #     if not fld.auto_created:
        #         self.helper[fld.name].update_attributes(placeholder=fld.verbose_name)
        #         if fld.help_text != '':
        #             self.helper[fld.name].update_attributes(title=fld.help_text)
        #             self.helper[fld.name].update_attributes(data_toggle="tooltip")

        self.render_hidden_fields = True
        self.form_show_labels = False
        self.use_custom_control = True
        self.form_tag = False
        self.disable_csrf = True


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
