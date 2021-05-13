from django.contrib import admin

from .models import Carousel, CarouselInfo, Featurette, FeaturetteInfo


class CarouselInfoInline(admin.TabularInline):
    model = CarouselInfo
    ordering = ['Language__Code', ]


class CarouselAdmin(admin.ModelAdmin):
    # list_display = ('SKU', 'Category', 'DateAdded', 'DateRemoved')
    # list_filter = ['Category']
    # list_editable = ['Category', 'DateAdded', 'DateRemoved']
    # ordering = ['SKU']
    inlines = [
        CarouselInfoInline,
    ]


class FeaturetteInfoInline(admin.TabularInline):
    model = FeaturetteInfo
    ordering = ['Language__Code', ]


class FeaturetteAdmin(admin.ModelAdmin):
    list_display = ('Slug',)
    # list_filter = ['Category']
    # list_editable = ['Category', 'DateAdded', 'DateRemoved']
    # ordering = ['SKU']
    inlines = [
        FeaturetteInfoInline,
    ]


admin.site.register(Carousel, CarouselAdmin)
admin.site.register(Featurette, FeaturetteAdmin)
