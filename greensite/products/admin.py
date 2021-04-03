from django.contrib import admin
from django.db import models

from martor.widgets import AdminMartorWidget

from .models import Currency, Language, Category, CategoryInfo, Product, ProductInfo, Tab, Price, Image


class LanguageAdmin(admin.ModelAdmin):
    list_display = ('Code', 'Name', 'Flag')
    list_editable = ['Name', 'Flag']
    ordering = ['Code']


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('Name', 'Order')
    list_editable = ['Order']
    ordering = ['Order']


class CategoryInfoAdmin(admin.ModelAdmin):
    list_display = ('Category', 'Language', 'Tagline')
    list_filter = ['Category', 'Language']
    list_editable = ['Tagline']
    ordering = ['Category__Name', 'Language__Code']


class ProductAdmin(admin.ModelAdmin):
    list_display = ('SKU', 'Category', 'DateAdded', 'DateRemoved')
    list_filter = ['Category']
    list_editable = ['Category', 'DateAdded', 'DateRemoved']
    ordering = ['SKU']


class ProductInfoAdmin(admin.ModelAdmin):
    list_display = ('Product', 'Language', 'Name', 'Specification')
    list_filter = ['Product', 'Language']
    list_editable = ['Name', 'Specification']
    ordering = ['Product__SKU', 'Language__Code']


class TabAdmin(admin.ModelAdmin):
    # fieldsets = [
    #     (None,               {'fields': ['question_text']}),
    #     ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    # ]
    formfield_overrides = {
        models.TextField: {'widget': AdminMartorWidget},
    }
    # inlines = [ChoiceInline]
    list_display = ('Product', 'Language', 'Order', 'Name', 'short_text')
    list_filter = ['Product', 'Language']
    list_editable = ['Order', 'Name']
    ordering = ['Product__SKU', 'Language__Code', 'Order']
    # search_fields = ['question_text']


class PriceAdmin(admin.ModelAdmin):
    list_display = ('Product', 'Currency', 'DateAdded', 'Price', 'PV')
    list_filter = ['Product', 'Currency']
    list_editable = ['DateAdded', 'Price', 'PV']
    ordering = ['Product__SKU', 'Currency__Code', 'DateAdded']


class ImageAdmin(admin.ModelAdmin):
    list_display = ('Product', 'Image', 'IsPrimary')
    list_filter = ['Product']
    ordering = ['Product__SKU', 'Image']


admin.site.register(Currency)
admin.site.register(Language, LanguageAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(CategoryInfo, CategoryInfoAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductInfo, ProductInfoAdmin)
admin.site.register(Tab, TabAdmin)
admin.site.register(Price, PriceAdmin)
admin.site.register(Image, ImageAdmin)