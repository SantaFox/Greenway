from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render

from .models import Language, Product, ProductInfo, Tab, Price, Image


def categories_view(request, name=None):
    return render(request, 'catalog/categories.html', {})


def products_view(request, category=None):
    products = Product.objects.all().order_by('SKU')
    return render(request, 'catalog/products.html', {'products': products})

# We have to comment it because generic.DetailView cannot process different # identifiers from URL
# class DetailView(generic.DetailView):
#     model = Product
#     template_name = 'catalog/detail.html'
def detail(request, productid=None, sku=None):
    # Work with selected language
    if not request.COOKIES.get('lang'):
        cookie_lang = ''
    else:
        cookie_lang = request.COOKIES.get('lang')

    if cookie_lang in ('eng', 'gr', 'ru'):
        detail_lang = cookie_lang
    else:
        detail_lang = 'eng'

    if productid:
        product = get_object_or_404(Product, pk=productid)
    elif sku:
        product = get_object_or_404(Product, SKU=sku)

    language = Language.objects.get(Code=detail_lang)

    languages = Language.objects.all().order_by('Code')

    product_info = ProductInfo.objects.get(Product=product, Language__Code=detail_lang)

    tabs = Tab.objects.filter(Product=product, Language__Code=detail_lang).order_by('Order')

    price = Price.objects.filter(Product=product).order_by('-DateAdded')[0]

    image_primary = Image.objects.get(Product=product, IsPrimary=True)

    response = render(request, 'catalog/detail.html', {
        'language': language,
        'languages': languages,
        'product': product,
        'product_info': product_info,
        'tabs': tabs,
        'price': price,
        'image_primary': image_primary,
    })
    if not request.COOKIES.get('lang'):
        response.set_cookie('lang', detail_lang)

    return response


def change_lang(request):
    if request.method == "POST":
        form_lang = request.POST['language']
        print(form_lang)
        response = HttpResponseRedirect(request.META['HTTP_REFERER'])
        if form_lang in ('eng', 'gr', 'ru'):
            response.set_cookie('lang', form_lang)
        else:
            response.set_cookie('lang', 'eng')
    else:
        response = HttpResponseRedirect(request.META['HTTP_REFERER'])

    return response
