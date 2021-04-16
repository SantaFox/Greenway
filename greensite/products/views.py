from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render
from django.db.models import Count, Q, FilteredRelation
from django.conf import settings
from django.urls import reverse
from django.utils import translation

from .models import Language, Category, Product, ProductInfo, Tab, Price, Image, Tag
from .forms import ProductForm, ProductInfoForm, TabForm, TabsFormset


def categories_view(request, name=None):
    return render(request, 'products/categories.html', {})


def list_all(request, category=None, tag=None):
    # Work with selected language
    cookie_lang = request.COOKIES.get(settings.LANGUAGE_COOKIE_NAME, settings.LANGUAGE_CODE)

    if cookie_lang in ('en', 'el', 'ru'):
        detail_lang = cookie_lang
    else:
        detail_lang = settings.LANGUAGE_CODE

    language = Language.objects.get(Code=detail_lang)
    languages = Language.objects.all().order_by('Code')

    ll = Product.objects.annotate(pi=FilteredRelation('productinfo', condition=Q(productinfo__Language=language.id))) \
        .values('SKU', 'Category__Name', 'Category__Slug', 'pi__Name').order_by('Category__Name', 'SKU') \
        .annotate(ImagesCount=Count('image', distinct=True)) \
        .annotate(TabsCount=Count('tab', distinct=True)) \
        .annotate(PricesCount=Count('price', distinct=True))

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
    cookie_lang = request.COOKIES.get(settings.LANGUAGE_COOKIE_NAME, settings.LANGUAGE_CODE)

    if cookie_lang in ('en', 'el', 'ru'):
        detail_lang = cookie_lang
    else:
        detail_lang = settings.LANGUAGE_CODE

    language = Language.objects.get(Code=detail_lang)
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
        'category': category,
        'products_list': final_set,
    })


def view_product(request, sku=None):
    # Work with selected language
    cookie_lang = request.COOKIES.get(settings.LANGUAGE_COOKIE_NAME, settings.LANGUAGE_CODE)

    if cookie_lang in ('en', 'el', 'ru'):
        detail_lang = cookie_lang
    else:
        detail_lang = settings.LANGUAGE_CODE

    language = Language.objects.get(Code=detail_lang)
    languages = Language.objects.all().order_by('Code')

    product = get_object_or_404(Product, SKU=sku)
    product_category = product.Category
    product_prev = Product.objects.filter(Category=product_category, SKU__lt=sku).order_by('-SKU').first()
    product_next = Product.objects.filter(Category=product_category, SKU__gt=sku).order_by('SKU').first()

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
        'prev': product_prev,
        'next': product_next,
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
        form_lang = request.POST.get('language', settings.LANGUAGE_CODE)
        response = HttpResponseRedirect(request.META['HTTP_REFERER'])
        if form_lang in ('en', 'el', 'ru'):
            translation.activate(form_lang)
            response.set_cookie(settings.LANGUAGE_COOKIE_NAME, form_lang)
        else:
            response.set_cookie(settings.LANGUAGE_COOKIE_NAME, settings.LANGUAGE_CODE)
    else:
        response = HttpResponseRedirect(request.META['HTTP_REFERER'])

    return response


@login_required
@permission_required('products.change_product', raise_exception=True)
def edit_product(request, blackbox=None):
    """View function for renewing a specific Product"""

    # Work with selected language
    cookie_lang = request.COOKIES.get(settings.LANGUAGE_COOKIE_NAME, settings.LANGUAGE_CODE)

    if cookie_lang in ('en', 'el', 'ru'):
        detail_lang = cookie_lang
    else:
        detail_lang = settings.LANGUAGE_CODE

    language = Language.objects.get(Code=detail_lang)
    languages = Language.objects.all().order_by('Code')

    product_instance = get_object_or_404(Product, SKU=blackbox)
    # related ProductInfo for this Product and Language may be absent
    try:
        product_info_instance = ProductInfo.objects.get(Product=product_instance, Language=language)
    except (ProductInfo.DoesNotExist, ProductInfo.MultipleObjectsReturned):
        product_info_instance = None
    # TODO: no ideas what to do here if there will be no tabs
    tabs_set = Tab.objects.filter(Product=product_instance, Language=language).order_by('Order')

    # If this is a POST request then process the Form data
    if request.method == 'POST':
        form_product = ProductForm(request.POST, prefix='fp', instance=product_instance)

        if product_info_instance:
            form_product_info = ProductInfoForm(request.POST, prefix='fpi', instance=product_info_instance)
        else:
            new_product_info = ProductInfo(Product=product_instance, Language=language)
            form_product_info = ProductInfoForm(request.POST, prefix='fpi', instance=new_product_info)

        if len(tabs_set) > 0:
            form_tab = TabForm(request.POST, prefix='ft', instance=tabs_set[0])
        else:
            new_tab = Tab(Product=product_instance, Language=language)
            form_tab = TabForm(request.POST, prefix='ft', instance=new_tab)

        # In theory, any of these three forms may be changed or not, but all three have to be valid
        if form_product.is_valid() and form_product_info.is_valid() and form_tab.is_valid():
            if form_product.has_changed():
                form_product.save()
            if form_product_info.has_changed():
                form_product_info.save()
            if form_tab.has_changed():
                form_tab.save()

            # redirect to a main product view
            # TODO: add some kind of information about it
            return HttpResponseRedirect(reverse('products:product', args=(blackbox,)))

    # If this is a GET (or any other method) create the default form.
    else:
        form_product = ProductForm(prefix='fp', instance=product_instance)
        form_product_info = ProductInfoForm(prefix='fpi', instance=product_info_instance)
        form_tabs = TabsFormset(prefix='fts', instance=product_instance, queryset=tabs_set)
        if len(tabs_set) > 0:
            form_tab = TabForm(prefix='ft', instance=tabs_set[0])
        else:
            form_tab = TabForm(prefix='ft')
            form_tab.fields['Order'].initial = 1
            form_tab.fields['Name'].initial = translation.pgettext('Default Tab name', 'Description')

    context = {
        'language': language,
        'languages': languages,
        'form_product': form_product,
        'form_product_info': form_product_info,
        'form_tabs': form_tabs,
        'form_tab': form_tab,
        'product_instance': product_instance,
    }

    return render(request, 'products/edit_product.html', context)
