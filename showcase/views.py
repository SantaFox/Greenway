from django.template.response import TemplateResponse

from greensite.decorators import prepare_languages

from .models import Carousel, CarouselInfo, Featurette, FeaturetteInfo

@prepare_languages
def view_index(request):
    carousels = Carousel.objects.filter(Active=True).order_by('Order')

    dict_carousel_infos = {ci.Carousel: ci for ci in
                          CarouselInfo.objects.filter(Carousel__Active=True, Language=request.language_instance)}

    carousel_set = []
    for caro in carousels:
        carousel_set.append(
            dict(carousel=caro,
                 carousel_info=dict_carousel_infos.get(caro),
                 )
        )

    featurettes = Featurette.objects.filter(Active=True).order_by('Order')

    dict_feat_infos = {fi.Featurette: fi for fi in
                          FeaturetteInfo.objects.filter(Featurette__Active=True, Language=request.language_instance)}

    feat_set = []
    for feat in featurettes:
        feat_set.append(
            dict(featurette=feat,
                 feat_info=dict_feat_infos.get(feat),
                 )
        )

    return TemplateResponse(request, 'showcase/index.html', {
        'carousels': carousel_set,
        'featurettes': feat_set,
    })

