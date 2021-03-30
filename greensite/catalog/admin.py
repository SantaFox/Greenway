from django.contrib import admin

from .models import Currency, Language, Product, ProductInfo, Tab


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
    list_display = ('Product', 'Language', 'Order', 'Name')
    list_filter = ['Product', 'Language']
    list_editable = ['Order', 'Name']
    ordering = ['Product__SKU', 'Language__Code']
    # search_fields = ['question_text']


admin.site.register(Currency)
admin.site.register(Language)
admin.site.register(Product)
admin.site.register(ProductInfo, ProductInfoAdmin)
admin.site.register(Tab, TabAdmin)
