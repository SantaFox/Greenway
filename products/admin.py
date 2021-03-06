from django.contrib import admin

from imagekit.admin import AdminThumbnail
from markdownx.admin import MarkdownxModelAdmin

from .models import Currency, Language, Action, ActionInfo, Category, CategoryInfo,\
    Product, ProductInfo, Tab, Price, Discount, Image, Tag, TagInfo


class LanguageAdmin(admin.ModelAdmin):
    list_display = ('Code', 'Name', 'Flag')
    list_editable = ['Name', 'Flag']
    ordering = ['Code']


# ************ InLine
class ActionInfoInline(admin.TabularInline):
    model = ActionInfo
    ordering = ['Language__Code', ]


class PriceInline(admin.TabularInline):
    model = Price
    exclude = ('GFT', )
    ordering = ['DateAdded', ]


class DiscountInline(admin.TabularInline):
    model = Discount
    ordering = ['Product__SKU', ]
# *******************************


class ActionAdmin(admin.ModelAdmin):
    list_display = ('DateAdded', 'Comment', 'DateStart', 'DateEnd')
    list_editable = ['Comment', 'DateStart', 'DateEnd']
    ordering = ['DateAdded']
    inlines = [
        DiscountInline,
        ActionInfoInline,
    ]


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('Name', 'Order', 'Slug')
    list_editable = ['Order', 'Slug']
    ordering = ['Order']


class CategoryInfoAdmin(admin.ModelAdmin):
    list_display = ('Category', 'Language', 'ShortDesc', 'Tagline')
    list_filter = ['Language', 'Category']
    list_editable = ['ShortDesc', 'Tagline']
    ordering = ['Category__Name', 'Language__Code']


class ProductAdmin(admin.ModelAdmin):
    list_display = ('SKU', 'Category', 'DateAdded', 'DateRemoved')
    list_filter = ['Category']
    list_editable = ['Category', 'DateAdded', 'DateRemoved']
    ordering = ['SKU']
    inlines = [
        PriceInline,
        DiscountInline,
    ]


class ProductInfoAdmin(admin.ModelAdmin):
    list_display = ('Product', 'Language', 'Name', 'Tagline', 'Specification')
    list_filter = ['Language', 'Product__Category', 'Product']
    list_editable = ['Name', 'Tagline', 'Specification']
    ordering = ['Product__Category__Name', 'Product__SKU', 'Language__Code']
    search_fields = ['Name', 'Specification']


class TabAdmin(MarkdownxModelAdmin):
    # fieldsets = [
    #     (None,               {'fields': ['question_text']}),
    #     ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    # ]
    # formfield_overrides = {
    #     models.TextField: {'widget': AdminPagedownWidget},
    # }
    # inlines = [ChoiceInline]
    list_display = ('Product', 'Language', 'Order', 'Name', 'short_text', 'TextQuality')
    list_filter = ['Language', 'Product']
    list_editable = ['Order', 'Name', 'TextQuality']
    ordering = ['Product__SKU', 'Language__Code', 'Order']
    # search_fields = ['question_text']


class PriceAdmin(admin.ModelAdmin):
    list_display = ('Product', 'DateAdded', 'Price', 'Currency', 'PV', 'Comment')
    list_filter = ['Currency', 'Product']
    list_editable = ['DateAdded', 'Price', 'Currency', 'PV', 'Comment']
    ordering = ['Product__SKU', 'Currency__Code', 'DateAdded']


class DiscountAdmin(admin.ModelAdmin):
    list_display = ('Product', 'Action', 'Price', 'Currency', 'PV', 'Comment')
    list_filter = ['Currency', 'Product__Category', 'Product']
    list_editable = ['Price', 'Currency', 'PV', 'Comment']
    ordering = ['Product__SKU', 'Currency__Code', 'Action__DateStart']


class ImageAdmin(admin.ModelAdmin):
    list_display = ('Product', 'Image', 'IsPrimary', 'admin_thumbnail')
    list_filter = ['Product']
    ordering = ['Product__SKU', 'Image']

    admin_thumbnail = AdminThumbnail(image_field='ImageAdminThumbnail')
    admin_thumbnail.short_description = 'Image'


class TagAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'Slug')
    list_editable = ['Slug']
    ordering = ['Slug']


class TagInfoAdmin(admin.ModelAdmin):
    list_display = ('Tag', 'Language', 'Name')
    list_filter = ['Language', 'Tag']
    list_editable = ['Name']
    ordering = ['Tag__Slug', 'Language__Code']


admin.site.register(Currency)
admin.site.register(Language, LanguageAdmin)
admin.site.register(Action, ActionAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(CategoryInfo, CategoryInfoAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductInfo, ProductInfoAdmin)
admin.site.register(Tab, TabAdmin)
admin.site.register(Price, PriceAdmin)
admin.site.register(Discount, DiscountAdmin)
admin.site.register(Image, ImageAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(TagInfo, TagInfoAdmin)
