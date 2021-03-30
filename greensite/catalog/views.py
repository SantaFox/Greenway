from django.shortcuts import render
from django.views import generic

from .models import Product, ProductInfo

# Create your views here.
class DetailView(generic.DetailView):
    model = Product
    template_name = 'catalog/detail.html'
