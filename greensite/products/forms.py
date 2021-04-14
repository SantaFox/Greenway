from django.forms import ModelForm, inlineformset_factory
from django.utils.translation import gettext_lazy as _

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Div, Field, Layout

from pagedown.widgets import PagedownWidget

from .models import Product, ProductInfo, Tab


class ProductForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                Field('Category', wrapper_class='col-md-4'),
                Field('DateAdded', wrapper_class='col-md-4'),
                Field('DateRemoved', wrapper_class='col-md-4'),
                css_class='form-row')
        )
        self.helper.form_tag = False        # We will use a common form
        self.helper.disable_csrf = True

    class Meta:
        model = Product
        fields = ['Category', 'DateAdded', 'DateRemoved']


class ProductInfoForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                Field('Name', wrapper_class='col-md-8'),
                Field('Specification', wrapper_class='col-md-4'),
                css_class='form-row')
        )
        self.helper.form_tag = False        # We will use a common form
        self.helper.disable_csrf = True

    class Meta:
        model = ProductInfo
        fields = ['Name', 'Specification']


class TabForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                Field('Order', wrapper_class='col-md-4'),
                Field('Name', wrapper_class='col-md-4'),
                Field('TextQuality', wrapper_class='col-md-4'),
                css_class='form-row'),
            Div(
                Field('Text'),
            )
        )
        self.helper.form_tag = False        # We will use a common form
        self.helper.disable_csrf = True
        self.helper.include_media = False

    class Meta:
        model = Tab
        fields = ['Order', 'Name', 'Text', 'TextQuality']
        widgets = {
            'Text': PagedownWidget,
        }


TabsFormset = inlineformset_factory(Product, Tab, TabForm, extra=1)
