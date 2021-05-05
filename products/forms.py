from django.forms import ModelForm, ModelMultipleChoiceField, CheckboxSelectMultiple, inlineformset_factory
from django.utils.translation import gettext_lazy as _

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Div, Field, Layout

from .models import Product, ProductInfo, Tab, Tag


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
        # self.helper.include_media = False

    class Meta:
        model = Tab
        fields = ['Order', 'Name', 'Text', 'TextQuality']


class TagForm(ModelForm):

    # Overriding __init__ here allows us to provide initial
    # data for 'toppings' field
    def __init__(self, *args, **kwargs):
        # Only in case we build the form from an instance
        # (otherwise, 'toppings' list should be empty)
        if kwargs.get('instance'):
            # The widget for a ModelMultipleChoiceField expects
            # a list of primary key for the selected data.
            tags_ids = [t.pk for t in kwargs['instance'].tags_of_product.all()]
            # We get the 'initial' keyword argument or initialize it
            # as a dict if it didn't exist.
            kwargs['initial'] = {
                'tags': tags_ids,
            }

        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        # self.helper.layout = Layout(
        #     Div(
        #         Field('Order', wrapper_class='col-md-4'),
        #         Field('Name', wrapper_class='col-md-4'),
        #         Field('TextQuality', wrapper_class='col-md-4'),
        #         css_class='form-row'),
        #     Div(
        #         Field('Text'),
        #     )
        # )
        self.helper.form_tag = False        # We will use a common form
        self.helper.disable_csrf = True

    # Overriding save allows us to process the value of 'toppings' field
    def save(self, commit=True):
        # Get the unsaved Pizza instance
        instance = ModelForm.save(self, False)

        # Prepare a 'save_m2m' method for the form,
        old_save_m2m = self.save_m2m

        def save_m2m():
            old_save_m2m()
            # This is where we actually link the pizza with toppings
            instance.tags_of_product.clear()
            instance.tags_of_product.add(*self.cleaned_data['tags'])

        self.save_m2m = save_m2m

        # Do we need to save all changes now?
        if commit:
            instance.save()
            self.save_m2m()

        return instance

    class Meta:
        model = Product
        fields = ('tags',)

    tags = ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=CheckboxSelectMultiple,
        required=False
    )


TabsFormset = inlineformset_factory(Product, Tab, TabForm, extra=1)
