from django.views import generic

from .models import Product


class DetailView(generic.DetailView):
    model = Product
    template_name = 'catalog/detail.html'
