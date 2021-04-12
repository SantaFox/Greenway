from django.db import models
from django.forms import ModelForm, inlineformset_factory

from .models import Product, ProductInfo, Tab


class ProductForm(ModelForm):
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
