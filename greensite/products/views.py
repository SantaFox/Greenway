from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render
from django.db.models import Count, Q, FilteredRelation

from .models import Language, Category, Product, ProductInfo, Tab, Price, Image, Tag


def categories_view(request, name=None):
    return render(request, 'products/categories.html', {})


def list_all(request, category=None, tag=None):
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

    ll = Product.objects.annotate(pi=FilteredRelation('productinfo', condition=Q(productinfo__Language=language.id))) \
        .values('SKU', 'Category__Name', 'pi__Name').order_by('Category__Name', 'SKU') \
        .annotate(ImagesCount=Count('image', distinct=True)) \
        .annotate(TabsCount=Count('tab', distinct=True))

    if category:
        ll = ll.filter(Category=category)

    if tag:
        ll = ll.filter(tag=tag)

    return render(request, 'products/list_all.html', {
        'language': language,
        'languages': languages,
        'products_list': ll,
    })


def list_products(request, category=None):
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

    products = Product.objects.filter(Category=category).order_by('SKU')
    dict_product_infos = {pi.Product: pi for pi in
                          ProductInfo.objects.filter(Product__Category=category, Language=language.id)}
    dict_images = {im.Product: im for im in Image.objects.filter(Product__Category=category, IsPrimary=True)}

    final_set = []  # list?
    for product in products:
        final_set.append(
            dict(product=product, product_info=dict_product_infos.get(product), image=dict_images.get(product)))

    return render(request, 'products/list_products.html', {
        'language': language,
        'languages': languages,
        'products_list': final_set,
    })


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

    tags = product.tag_set.all().annotate(
        tagname=FilteredRelation('taginfo', condition=Q(taginfo__Language=language.id))) \
        .values('tagname__Name').order_by('tagname__Name')

    response = render(request, 'products/view_product.html', {
        'language': language,
        'languages': languages,
        'product': product,
        'product_info': product_info,
        'tabs': tabs,
        'price': price,
        'image_primary': image_primary,
        'tags': tags,
    })
    if not request.COOKIES.get('lang'):
        response.set_cookie('lang', detail_lang)

    return response


def product_dispatch(request, blackbox=None):
    # Now we are trying to realize what is "blackbox" were passed
    try:
        category = Category.objects.get(Slug=blackbox)
        return list_products(request, category=category)
    except (Category.DoesNotExist, Category.MultipleObjectsReturned):
        category = None  # Just in case

    try:
        tag = Tag.objects.get(Slug=blackbox)
        return list_all(request, tag=tag)
    except (Tag.DoesNotExist, Tag.MultipleObjectsReturned):
        tag = None  # Just in case

    try:
        product = Product.objects.get(SKU=blackbox)
        # TODO: Decide should it be replaced to passing a product object
        return view_product(request, sku=blackbox)
    except (Product.DoesNotExist, Product.MultipleObjectsReturned):
        product = None  # Just in case

    raise Http404()

    return


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
