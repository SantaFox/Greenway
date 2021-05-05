from django.utils.translation import gettext_lazy as _

import django_filters

from .models import CustomerOrder

# https://django-filter.readthedocs.io/en/stable/guide/usage.html


class CustomerOrderFilter(django_filters.FilterSet):

    Customer__Name = django_filters.CharFilter(label=_("Customer Name"), lookup_expr='icontains', )

    ShowClosed = django_filters.BooleanFilter(label=_('Show settled Orders'), method='filter_closed_orders')
    #
    # class Meta:
    #     model = CustomerOrder
    #     fields = ['Customer',]

    def filter_closed_orders(self, queryset, name, value):
        return queryset.filter(**{
            name: value,
        })