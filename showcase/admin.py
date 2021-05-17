from django.contrib import admin

from .models import Carousel, CarouselInfo, Featurette, FeaturetteInfo


class CarouselInfoInline(admin.TabularInline):
    model = CarouselInfo
    ordering = ['Language__Code', ]


class CarouselAdmin(admin.ModelAdmin):
    list_display = ('Order', 'Slug', 'Active', 'Image', 'ButtonAction', 'HeaderClass', 'TextClass', )
    # list_filter = ['Category']
    list_editable = ['Active', 'ButtonAction', 'HeaderClass', 'TextClass', ]
    ordering = ['Order']
    inlines = [
        CarouselInfoInline,
    ]


class FeaturetteInfoInline(admin.TabularInline):
    model = FeaturetteInfo
    ordering = ['Language__Code', ]


class FeaturetteAdmin(admin.ModelAdmin):
    list_display = ('Order', 'Slug', 'Active', 'Image', )
    # list_filter = ['Category']
    list_editable = ['Slug', 'Active']
    ordering = ['Order']
    inlines = [
        FeaturetteInfoInline,
    ]


admin.site.register(Carousel, CarouselAdmin)
admin.site.register(Featurette, FeaturetteAdmin)
