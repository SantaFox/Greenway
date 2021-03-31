from django.contrib import admin

from .models import Currency, Language, Product, ProductInfo, Tab, Price


class LanguageAdmin(admin.ModelAdmin):
    list_display = ('Code', 'Name')
    list_editable = ['Name']
    ordering = ['Code']


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


admin.site.register(Currency)
admin.site.register(Language, LanguageAdmin)
admin.site.register(Product)
admin.site.register(ProductInfo, ProductInfoAdmin)
admin.site.register(Tab, TabAdmin)
admin.site.register(Price, PriceAdmin)
