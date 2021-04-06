from django.db import models
from django.template.defaultfilters import truncatechars  # or truncatewords
from martor.models import MartorField
from imagekit.models import ImageSpecField

from .imagegenerators import AdminThumbnailSpec


# System classes below
class Language(models.Model):
    Code = models.CharField(max_length=3, blank=False)
    Name = models.CharField(max_length=50, blank=False)
    Flag = models.CharField(max_length=10, blank=False)
    TimestampCreated = models.DateTimeField(auto_now_add=True)
    TimestampModified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.Code

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['Code'], name='unique_Language')
        ]


class Currency(models.Model):
    Code = models.CharField(max_length=3, blank=False)
    Symbol = models.CharField(max_length=1, blank=True)
    TimestampCreated = models.DateTimeField(auto_now_add=True)
    TimestampModified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.Code

    class Meta:
        verbose_name_plural = "Currencies"
        constraints = [
            models.UniqueConstraint(fields=['Code'], name='unique_Currency')
        ]


# Data classes below
class Category(models.Model):
    Name = models.CharField(max_length=50, blank=False)
    Slug = models.SlugField(blank=False)
    Order = models.IntegerField(blank=False)
    TimestampCreated = models.DateTimeField(auto_now_add=True)
    TimestampModified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.Name

    class Meta:
        verbose_name_plural = "Categories"
        constraints = [
            models.UniqueConstraint(fields=['Order'], name='unique_Category')
        ]


class CategoryInfo(models.Model):
    Category = models.ForeignKey(Category, on_delete=models.PROTECT)
    Language = models.ForeignKey(Language, on_delete=models.PROTECT)
    Tagline = models.CharField(max_length=255, blank=False)
    TimestampCreated = models.DateTimeField(auto_now_add=True)
    TimestampModified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.Category} / {self.Language} / {self.Tagline}'

    class Meta:
        verbose_name_plural = "Categories Info"
        constraints = [
            models.UniqueConstraint(fields=['Category', 'Language'], name='unique_CategoryInfo')
        ]


class Product(models.Model):
    Category = models.ForeignKey(Category, on_delete=models.PROTECT)
    SKU = models.CharField(max_length=50, blank=False)
    DateAdded = models.DateField(blank=True, null=True)
    DateRemoved = models.DateField(blank=True, null=True)
    TimestampCreated = models.DateTimeField(auto_now_add=True)
    TimestampModified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.SKU

    def ordered_price_set(self):
        return self.price_set.all().order_by('DateAdded')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['SKU'], name='unique_Product')
        ]


class ProductInfo(models.Model):
    Product = models.ForeignKey(Product, on_delete=models.PROTECT)
    Language = models.ForeignKey(Language, on_delete=models.PROTECT)
    Name = models.CharField(max_length=255, blank=False)
    Specification = models.CharField(max_length=255, blank=True)
    TimestampCreated = models.DateTimeField(auto_now_add=True)
    TimestampModified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.Product} / {self.Language} / {self.Name}'

    class Meta:
        verbose_name_plural = "Products Info"
        constraints = [
            models.UniqueConstraint(fields=['Product', 'Language'], name='unique_ProductInfo')
        ]


class Tab(models.Model):
    Product = models.ForeignKey(Product, on_delete=models.PROTECT)
    Language = models.ForeignKey(Language, on_delete=models.PROTECT)
    Order = models.IntegerField(blank=False)
    Name = models.CharField(max_length=255, blank=False)
    Text = MartorField(blank=True)
    TextQuality = models.IntegerField(choices=[
        (0, 'Not tested'),
        (1, 'Low quality'),
        (2, 'Medium quality'),
        (3, 'Good quality'),
    ], default=0)
    TimestampCreated = models.DateTimeField(auto_now_add=True)
    TimestampModified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.Product} / {self.Language} / {self.Order} / {self.Name}'

    @property
    def short_text(self):
        return truncatechars(self.Text, 100)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['Product', 'Language', 'Order'], name='unique_Tab')
        ]


class Price(models.Model):
    Product = models.ForeignKey(Product, on_delete=models.PROTECT)
    Currency = models.ForeignKey(Currency, on_delete=models.PROTECT)
    DateAdded = models.DateField(blank=True, null=True)
    Price = models.DecimalField(max_digits=7, decimal_places=2, blank=False)
    PV = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    TimestampCreated = models.DateTimeField(auto_now_add=True)
    TimestampModified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.Product} / {self.Currency} / {self.DateAdded} / {self.Price} / {self.PV}'

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['Product', 'Currency', 'DateAdded'], name='unique_Price')
        ]


class Image(models.Model):
    Product = models.ForeignKey(Product, on_delete=models.PROTECT)
    Image = models.ImageField()
    IsPrimary = models.BooleanField(default=False)
    ImageAdminThumbnail = ImageSpecField(source='Image', spec=AdminThumbnailSpec)
    TimestampCreated = models.DateTimeField(auto_now_add=True)
    TimestampModified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.Image.name

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['Image'], name='unique_ImageName')
        ]


class Tag(models.Model):
    Product = models.ManyToManyField(Product, blank=True)
    Slug = models.SlugField(blank=False)
    TimestampCreated = models.DateTimeField(auto_now_add=True)
    TimestampModified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.Slug} / {len(self.Product.all())} product(s)'


class TagInfo(models.Model):
    Tag = models.ForeignKey(Tag, on_delete=models.PROTECT)
    Language = models.ForeignKey(Language, on_delete=models.PROTECT)
    Name = models.CharField(max_length=255, blank=False)
    TimestampCreated = models.DateTimeField(auto_now_add=True)
    TimestampModified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.Tag} / {self.Language} / {self.Name}'

    class Meta:
        verbose_name_plural = "Tags Info"
        constraints = [
            models.UniqueConstraint(fields=['Tag', 'Language'], name='unique_TagInfo')
        ]
