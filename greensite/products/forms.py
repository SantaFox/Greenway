from django.db import models
from django.forms import ModelForm, inlineformset_factory
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Div, Field, Layout

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

    class Meta:
        model = Product
        fields = ['Category', 'DateAdded', 'DateRemoved']


class ProductInfoForm(ModelForm):
    class Meta:
        model = ProductInfo
        fields = ['Name', 'Specification']


class TabForm(ModelForm):
    class Meta:
        model = Tab
        fields = ['Order', 'Name', 'Text', 'TextQuality']


TabsFormset = inlineformset_factory(Product, Tab, TabForm, extra=1)
