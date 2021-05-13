from django.db import models
from django.utils.translation import gettext_lazy as _

from imagekit.models import ImageSpecField

from products.models import Language


class Carousel(models.Model):
    Slug = models.SlugField(blank=False)
    Active = models.BooleanField(default=False)

    Image = models.ImageField(upload_to='carousel/')
    # ImageAdminThumbnail = ImageSpecField(source='Image', spec=AdminThumbnailSpec)

    TimestampCreated = models.DateTimeField(auto_now_add=True)
    TimestampModified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.Slug

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['Slug'], name='unique_Carousel')
        ]


class CarouselInfo(models.Model):
    Carousel = models.ForeignKey(Carousel, on_delete=models.PROTECT)
    Language = models.ForeignKey(Language, on_delete=models.PROTECT)

    Header = models.CharField(max_length=255, blank=True)
    Text = models.TextField(blank=True)

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
    Slug = models.SlugField(blank=False)
    Active = models.BooleanField(default=False)

    Image = models.ImageField(upload_to='featurette/')
    # ImageAdminThumbnail = ImageSpecField(source='Image', spec=AdminThumbnailSpec)

    TimestampCreated = models.DateTimeField(auto_now_add=True)
    TimestampModified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.Slug

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['Slug'], name='unique_Featurette')
        ]


class FeaturetteInfo(models.Model):
    Featurette = models.ForeignKey(Featurette, on_delete=models.PROTECT)
    Language = models.ForeignKey(Language, on_delete=models.PROTECT)

    Header = models.CharField(max_length=255, blank=True)
    Text = models.TextField(blank=True)

    TimestampCreated = models.DateTimeField(auto_now_add=True)
    TimestampModified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.Featurette} / {self.Language} / {self.Header}'

    class Meta:
        verbose_name_plural = "Featurettes Info"
        constraints = [
            models.UniqueConstraint(fields=['Featurette', 'Language'], name='unique_FeaturetteInfo')
        ]
