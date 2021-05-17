from django.db import models
from django.utils.translation import gettext_lazy as _

from imagekit.models import ImageSpecField

from products.models import Language


class Carousel(models.Model):
    Order = models.IntegerField(blank=False)
    Slug = models.SlugField(blank=False)
    Active = models.BooleanField(default=False)

    Image = models.ImageField(upload_to='carousel/')
    # ImageAdminThumbnail = ImageSpecField(source='Image', spec=AdminThumbnailSpec)

    ButtonAction = models.CharField(max_length=255, blank=True,
                                    verbose_name=_('Button Action'),
                                    help_text=_(
                                        'Action fired when carousel button is pressed. If empty, no button is shown.'))

    HeaderClass = models.CharField(max_length=255, blank=True,
                                   verbose_name=_('Header Class'),
                                   help_text=_(
                                      'Bootstrap class for header over image. May be used for color change.'))

    TextClass = models.CharField(max_length=255, blank=True,
                                 verbose_name=_('Text Class'),
                                 help_text=_(
                                    'Bootstrap class for text over image. May be used for color change.'))

    TimestampCreated = models.DateTimeField(auto_now_add=True)
    TimestampModified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.Slug

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['Order'], name='unique_Carousel')
        ]


class CarouselInfo(models.Model):
    Carousel = models.ForeignKey(Carousel, on_delete=models.PROTECT)
    Language = models.ForeignKey(Language, on_delete=models.PROTECT)

    Header = models.CharField(max_length=255, blank=True)
    Text = models.TextField(blank=True)

    ButtonText = models.CharField(max_length=50, blank=True, verbose_name=_('Button Text'),
                                  help_text=_('Text shown on the carousel text block'))

    TimestampCreated = models.DateTimeField(auto_now_add=True)
    TimestampModified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.Carousel} / {self.Language} / {self.Header}'

    class Meta:
        verbose_name_plural = "Carousels Info"
        constraints = [
            models.UniqueConstraint(fields=['Carousel', 'Language'], name='unique_CarouselInfo')
        ]


class Featurette(models.Model):
    Order = models.IntegerField(blank=False)
    Slug = models.SlugField(blank=False)
    Active = models.BooleanField(default=False)

    Image = models.ImageField(upload_to='featurette/')
    # ImageAdminThumbnail = ImageSpecField(source='Image', spec=AdminThumbnailSpec)

    ButtonAction = models.CharField(max_length=255, blank=True,
                                    verbose_name=_('Button Action'),
                                    help_text=_(
                                        'Action fired when featurette button is pressed. If empty, no button is shown.'))

    TimestampCreated = models.DateTimeField(auto_now_add=True)
    TimestampModified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.Slug

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['Order'], name='unique_Featurette')
        ]


class FeaturetteInfo(models.Model):
    Featurette = models.ForeignKey(Featurette, on_delete=models.PROTECT)
    Language = models.ForeignKey(Language, on_delete=models.PROTECT)

    Header = models.CharField(max_length=255, blank=True)
    Text = models.TextField(blank=True)

    ButtonText = models.CharField(max_length=50, blank=True, verbose_name=_('Button Text'),
                                  help_text=_('Text shown on the '))

    TimestampCreated = models.DateTimeField(auto_now_add=True)
    TimestampModified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.Featurette} / {self.Language} / {self.Header}'

    class Meta:
        verbose_name_plural = "Featurettes Info"
        constraints = [
            models.UniqueConstraint(fields=['Featurette', 'Language'], name='unique_FeaturetteInfo')
        ]
