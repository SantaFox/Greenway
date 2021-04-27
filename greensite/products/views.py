from datetime import datetime

from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponseRedirect, Http404
from django.template.response import TemplateResponse
from django.shortcuts import get_object_or_404, render
from django.db.models import Count, Max, Q, FilteredRelation
from django.conf import settings
from django.urls import reverse
from django.utils import translation

from greensite.decorators import prepare_languages

from .models import Language, Category, Product, ProductInfo, Tab, Price, Image, Tag, TagInfo
from .forms import ProductForm, ProductInfoForm, TabForm, TagForm, TabsFormset


def categories_view(request, name=None):
    return render(request, 'products/categories.html', {})


@prepare_languages
def list_all(request, category=None, tag=None):
    ll = Product.objects \
        .annotate(pi=FilteredRelation('productinfo', condition=Q(productinfo__Language=request.language_instance))) \
        .values('SKU', 'Category__Name', 'Category__Slug', 'pi__Name').order_by('Category__Name', 'SKU') \
        .annotate(ImagesCount=Count('image', distinct=True)) \
        .annotate(TabsCount=Count('tab', distinct=True)) \
        .annotate(PricesCount=Count('price', distinct=True))

    if category:
        ll = ll.filter(Category=category)

    if tag:
        ll = ll.filter(tags_of_product=tag)

    return TemplateResponse(request, 'products/list_all.html', {
        'products_list': ll,
    })


@prepare_languages
def list_products(request, category=None):
    products = Product.objects.filter(Category=category).order_by('SKU')

    dict_product_infos = {pi.Product: pi for pi in
                          ProductInfo.objects.filter(Product__Category=category, Language=request.language_instance)}

    dict_images = {im.Product: im for im in Image.objects.filter(Product__Category=category, IsPrimary=True)}

    # Цен может быть от 0 до много, надо вытащить самую "близкую" или NONE, и дальше собрать в словаре
    # Самое красивое решение - здаесь: https://stackoverflow.com/questions/59893756/django-group-by-one-field-only-take-the-latest-max-of-each-group-and-get-bac
    # Но к сожалению SQLite backend не поддерживает команду DISTINCT ON (fields), поэтому делаем менее красивое решение
    # Важно: уникальный ключ - продукт + дата цены + **ВАЛЮТА**
    dict_price_distinct = Price.objects \
        .filter(Product__Category=category) \
        .values('Product_id', 'Currency_id') \
        .annotate(max_date=Max('DateAdded')) \
        .order_by()
    dict_price_list = list(dict_price_distinct)

    dict_prices = {prc.Product: prc for prc in Price.objects.filter(Product__Category=category) if
                   # Creating main unique index
                   {'Product_id': prc.Product_id,
                    'Currency_id': prc.Currency_id,
                    'max_date': prc.DateAdded
                    } in dict_price_list
                   }

    # And final step, we need tags for each product. It may be None or one or several Tags
    # We also need translations, as instances if possible
    tags_distinct = Tag.objects.filter(Product__Category=category).distinct()

    dict_tag_infos = {ti.Tag: ti for ti in TagInfo.objects.filter(Language=request.language_instance)}

    dict_tags = {}
    for t in tags_distinct:
        new_tag_instance = {'tag': t, 'tag_info': dict_tag_infos[t]}
        for p in t.Product.filter(Category=category):
            if dict_tags.get(p):
                dict_tags[p].append(new_tag_instance)
            else:
                dict_tags[p] = [new_tag_instance, ]

    final_set = []
    for product in products:
        final_set.append(
            dict(product=product,
                 product_info=dict_product_infos.get(product),
                 image=dict_images.get(product),
                 price=dict_prices.get(product),
                 tags=dict_tags.get(product),
                 )
        )

    return TemplateResponse(request, 'products/list_products.html', {
        'category': category,
        'products_list': final_set,
    })


@prepare_languages
def view_product(request, sku=None):
    product = get_object_or_404(Product, SKU=sku)
    product_category = product.Category
    product_prev = Product.objects.filter(Category=product_category, SKU__lt=sku).order_by('-SKU').first()
    product_next = Product.objects.filter(Category=product_category, SKU__gt=sku).order_by('SKU').first()

    try:
        product_info = ProductInfo.objects.get(Product=product, Language=request.language_instance)
    except (ProductInfo.DoesNotExist, ProductInfo.MultipleObjectsReturned):
        product_info = None

    tabs = Tab.objects.filter(Product=product, Language=request.language_instance).order_by('Order')

    prices = Price.objects.filter(Product=product, DateAdded__lte=datetime.now()).order_by('-DateAdded')
    price = prices.first()  # First or None

    try:
        image_primary = Image.objects.get(Product=product, IsPrimary=True)
    except (Image.DoesNotExist, Image.MultipleObjectsReturned):
        image_primary = None

    # We expect here a queryset from empty to many. The problem is that the classic FilteredRelation with condition
    # will product a values queryset while we prefer an instance queryset
    # tags = product.tags_of_product.all().annotate(
    #     tagname=FilteredRelation('taginfo', condition=Q(taginfo__Language=language.id))) \
    #     .values('tagname__Name').order_by('tagname__Name')
    tags = Tag.objects.filter(Product=product)
    dict_tags_info = {ti.Tag: ti for ti in TagInfo.objects.filter(Tag__Product=product, Language=request.language_instance)}

    tags_final_set = []
    for tag in tags:
        tags_final_set.append(
            dict(tag=tag,
                 tag_info=dict_tags_info.get(tag),
                 )
        )

    return TemplateResponse(request, 'products/view_product.html', {
        'product': product,
        'product_prev': product_prev,
        'product_next': product_next,
        'product_info': product_info,
        'tabs': tabs,
        'price': price,
        'prices': prices,
        'image_primary': image_primary,
        'tags': tags_final_set,
    })


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
@prepare_languages
def edit_product(request, blackbox=None):
    product_instance = get_object_or_404(Product, SKU=blackbox)
    # related ProductInfo for this Product and Language may be absent
    try:
        product_info_instance = ProductInfo.objects.get(Product=product_instance, Language=request.language_instance)
    except (ProductInfo.DoesNotExist, ProductInfo.MultipleObjectsReturned):
        product_info_instance = None
    # TODO: no ideas what to do here if there will be no tabs
    tabs_set = Tab.objects.filter(Product=product_instance, Language=request.language_instance).order_by('Order')

    # If this is a POST request then process the Form data
    if request.method == 'POST':
        form_product = ProductForm(request.POST, prefix='fp', instance=product_instance)

        if product_info_instance:
            form_product_info = ProductInfoForm(request.POST, prefix='fpi', instance=product_info_instance)
        else:
            new_product_info = ProductInfo(Product=product_instance, Language=request.language_instance)
            form_product_info = ProductInfoForm(request.POST, prefix='fpi', instance=new_product_info)

        if len(tabs_set) > 0:
            form_tab = TabForm(request.POST, prefix='ft', instance=tabs_set[0])
        else:
            new_tab = Tab(Product=product_instance, Language=request.language_instance)
            form_tab = TabForm(request.POST, prefix='ft', instance=new_tab)

        form_tags = TagForm(request.POST, prefix='ftg', instance=product_instance)

        # In theory, any of these three forms may be changed or not, but all three have to be valid
        if form_product.is_valid() and form_product_info.is_valid() and form_tab.is_valid() and form_tags.is_valid():
            if form_product.has_changed():
                form_product.save()
            if form_product_info.has_changed():
                form_product_info.save()
            if form_tab.has_changed() and form_tab.cleaned_data['Text'] != '':
                form_tab.save()
            if form_tags.has_changed():
                form_tags.save()

            # redirect to a main product view
            # TODO: add some kind of information about it
            return HttpResponseRedirect(reverse('products:product', args=(blackbox,)))

    # If this is a GET (or any other method) create the default form.
    else:
        form_product = ProductForm(prefix='fp', instance=product_instance)
        form_product_info = ProductInfoForm(prefix='fpi', instance=product_info_instance)
        form_tabs = TabsFormset(prefix='fts', instance=product_instance, queryset=tabs_set)
        form_tags = TagForm(prefix='ftg', instance=product_instance)

        if len(tabs_set) > 0:
            form_tab = TabForm(prefix='ft', instance=tabs_set[0])
        else:
            form_tab = TabForm(prefix='ft')
            form_tab.fields['Order'].initial = 1
            form_tab.fields['Name'].initial = translation.pgettext('Default Tab name', 'Description')

    return TemplateResponse(request, 'products/edit_product.html', {
        'form_product': form_product,
        'form_product_info': form_product_info,
        'form_tabs': form_tabs,
        'form_tab': form_tab,
        'form_tags': form_tags,
        'product_instance': product_instance,
    })
