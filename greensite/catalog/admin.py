from django.contrib import admin

from .models import Currency, Language, Group, GroupInfo, Product, ProductInfo, Tab, Price, Image


class LanguageAdmin(admin.ModelAdmin):
    list_display = ('Code', 'Name')
    list_editable = ['Name']
    ordering = ['Code']


class GroupAdmin(admin.ModelAdmin):
    list_display = ('Name', 'Order')
    list_editable = ['Order']
    ordering = ['Order']


class GroupInfoAdmin(admin.ModelAdmin):
    list_display = ('Group', 'Language', 'Tagline')
    list_filter = ['Group', 'Language']
    list_editable = ['Tagline']
    ordering = ['Group__Name', 'Language__Code']


class ProductAdmin(admin.ModelAdmin):
    list_display = ('Group', 'SKU')
    list_display_links = ['SKU']
    list_filter = ['Group']
    # list_editable = ['Group']
    ordering = ['Group']


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


class ImageAdmin(admin.ModelAdmin):
    list_display = ('Product', 'Image', 'IsPrimary')
    list_filter = ['Product']
    ordering = ['Product__SKU', 'Image']


admin.site.register(Currency)
admin.site.register(Language, LanguageAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(GroupInfo, GroupInfoAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductInfo, ProductInfoAdmin)
admin.site.register(Tab, TabAdmin)
admin.site.register(Price, PriceAdmin)
admin.site.register(Image, ImageAdmin)