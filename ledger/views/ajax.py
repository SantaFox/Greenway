from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Q
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.http import require_GET

from products.models import Product

from ledger.models import Counterparty


# @login_required
# @require_GET
# @permission_required('products.view_product', raise_exception=True)
def counterparty_search(request):
    qry = Counterparty.objects.filter(User=request.user)
    search = request.GET.get('q', '')
    qry_filter = Q(Name__icontains=search) |\
                 Q(Email__icontains=search) |\
                 Q(Telegram__icontains=search) | \
                 Q(Instagram__icontains=search) | \
                 Q(Facebook__icontains=search) | \
                 Q(City__icontains=search) | \
                 Q(Address__icontains=search) | \
                 Q(Memo__icontains=search)

    response_dict = [
        {"id": cp.pk,
         "text": cp.Name
         } for cp in qry.filter(qry_filter).order_by('Name').distinct()
    ]
    return JsonResponse({'results': response_dict}, safe=False)


@login_required
@require_GET
# @permission_required('products.view_product', raise_exception=True)
def product_search(request):
    qry = Product.objects.all()
    search = request.GET.get('q', '')
    qry_filter = Q(SKU__icontains=search) |\
                 Q(Category__Name__icontains=search) |\
                 Q(productinfo__Name__icontains=search)

    response_dict = [
        {"id": cp.pk,
         "text": cp.get_full_name(),
         "price": cp.get_price_on_date(timezone.now()),
         } for cp in qry.filter(qry_filter).order_by('SKU').distinct()
    ]
    return JsonResponse({'results': response_dict}, safe=False)
