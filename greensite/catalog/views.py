from django.views import generic
from django.shortcuts import get_object_or_404, render

from .models import Product


# We have to comment it because generic.DetailView cannot process different
# identifiers from URL
# class DetailView(generic.DetailView):
#     model = Product
#     template_name = 'catalog/detail.html'

def detail(request, productid=None, sku=None):
    if productid:
        product = get_object_or_404(Product, pk=productid)
    elif sku:
        product = get_object_or_404(Product, SKU=sku)

    return render(request, 'catalog/detail.html', {'product': product})
