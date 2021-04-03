from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.db.models import Count, Q, FilteredRelation

from .models import Language, Product, ProductInfo, Tab, Price, Image


def categories_view(request, name=None):
    return render(request, 'products/categories.html', {})


def list_all(request):
    # Work with selected language
    if not request.COOKIES.get('lang'):
        cookie_lang = ''
    else:
        cookie_lang = request.COOKIES.get('lang')

    if cookie_lang in ('eng', 'gr', 'ru'):
        view_lang = cookie_lang
    else:
        view_lang = 'eng'

    language = Language.objects.get(Code=view_lang)
    languages = Language.objects.all().order_by('Code')

    ll = Product.objects.annotate(pi=FilteredRelation('productinfo', condition=Q(productinfo__Language=language.id)))\
        .values('SKU', 'Group__Name', 'pi__Name').order_by('Group__Name', 'SKU')\
        .annotate(ImagesCount=Count('image'))

    return render(request, 'products/list_all.html', {
        'language': language,
        'languages': languages,
        'products_list': ll,
    })


# We have to comment it because generic.DetailView cannot process different # identifiers from URL
# class DetailView(generic.DetailView):
#     model = Product
#     template_name = 'catalog/detail.html'
def view_product(request, sku=None):
    # Work with selected language
    if not request.COOKIES.get('lang'):
        cookie_lang = ''
    else:
        cookie_lang = request.COOKIES.get('lang')

    if cookie_lang in ('eng', 'gr', 'ru'):
        detail_lang = cookie_lang
    else:
        detail_lang = 'eng'

    product = get_object_or_404(Product, SKU=sku)

    language = Language.objects.get(Code=detail_lang)
    languages = Language.objects.all().order_by('Code')

    try:
        product_info = ProductInfo.objects.get(Product=product, Language__Code=detail_lang)
    except (ProductInfo.DoesNotExist, ProductInfo.MultipleObjectsReturned):
        product_info = None

    tabs = Tab.objects.filter(Product=product, Language__Code=detail_lang).order_by('Order')

    price_hist = Price.objects.filter(Product=product).order_by('-DateAdded')
    if price_hist:
        price = price_hist[0]
    else:
        price = None

    try:
        image_primary = Image.objects.get(Product=product, IsPrimary=True)
    except (Image.DoesNotExist, Image.MultipleObjectsReturned):
        image_primary = None

    response = render(request, 'products/view_product.html', {
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
