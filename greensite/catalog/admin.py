from django.contrib import admin

from .models import Currency, Language, Product, ProductInfo, Tab


class TabAdmin(admin.ModelAdmin):
    # fieldsets = [
    #     (None,               {'fields': ['question_text']}),
    #     ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    # ]
    # inlines = [ChoiceInline]
    list_display = ('Product', 'Language', 'Order', 'Name')
    list_filter = ['Product', 'Language']
    list_editable = ['Order', 'Name']
    ordering = ['Product', 'Language', 'Order']
    # search_fields = ['question_text']


admin.site.register(Currency)
admin.site.register(Language)
admin.site.register(Product)
admin.site.register(ProductInfo)
admin.site.register(Tab, TabAdmin)
