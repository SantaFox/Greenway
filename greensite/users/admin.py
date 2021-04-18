from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import GreenwayUser


class GreenwayUserAdmin(UserAdmin):

    def __init__(self, *args, **kwargs):
        super(UserAdmin, self).__init__(*args, **kwargs)

        UserAdmin.list_display = list(UserAdmin.list_display) + ['ManagingPartner', 'ReferralCode']
        UserAdmin.fieldsets = UserAdmin.fieldsets + (
            ('Greenway-Specific Data', {'fields': ('ManagingPartner', 'ReferralCode',)}),
        )


admin.site.register(GreenwayUser, GreenwayUserAdmin)
