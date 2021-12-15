from django.db import models
from django.template.defaultfilters import truncatechars  # or truncatewords
from django.utils.translation import gettext_lazy as _
from django.db.models import Q, F

from imagekit.models import ImageSpecField
from markdownx.models import MarkdownxField
from markdownx.utils import markdownify

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
class Action(models.Model):
    DateAdded = models.DateField(blank=False, null=False, verbose_name=_('Date Added'),
                                 help_text=_('Date when this action is published'))
    DateStart = models.DateTimeField(blank=False, null=False)
    DateEnd = models.DateTimeField(blank=False, null=False)
    Comment = models.CharField(max_length=100, blank=True)  # may be replaced later with real slug

    TimestampCreated = models.DateTimeField(auto_now_add=True)
    TimestampModified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.DateAdded} / {self.Comment}'

    class Meta:
        verbose_name_plural = "Actions"


class ActionInfo(models.Model):
    Action = models.ForeignKey(Action, on_delete=models.PROTECT)
    Language = models.ForeignKey(Language, on_delete=models.PROTECT)

    Header = models.CharField(max_length=100, blank=False)
    SubHeader = models.CharField(max_length=100, blank=True)
    Text = MarkdownxField(blank=True)

    TimestampCreated = models.DateTimeField(auto_now_add=True)
    TimestampModified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.Category} / {self.Language} / {self.Tagline}'

    class Meta:
        verbose_name_plural = "Actions Info"
        constraints = [
            models.UniqueConstraint(fields=['Action', 'Language'], name='unique_ActionInfo')
        ]


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

    ShortDesc = models.CharField(max_length=100, blank=False)
    LongDesc = models.CharField(max_length=100, blank=True)
    Tagline = models.CharField(max_length=255, blank=True)

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
    Category = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name=_('Category'),
                                 help_text=_('Category to which this product belongs'))
    SKU = models.CharField(max_length=50, blank=False)

    DateAdded = models.DateField(blank=True, null=True, verbose_name=_('Date Added'),
                                 help_text=_('Date when this product became available to public'))
    DateRemoved = models.DateField(blank=True, null=True, verbose_name=_('Date Removed'),
                                   help_text=_('Date when this product became unavailable to order'))

    SetProducts = models.ManyToManyField("self", blank=True, symmetrical=False)

    TimestampCreated = models.DateTimeField(auto_now_add=True)
    TimestampModified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.SKU

    def ordered_price_set(self):
        return self.price_set.all().order_by('DateAdded')

    def get_price_on_date(self, date):
        discounts = Discount.objects.filter(Product=self, DateStart__lte=date, DateEnd__gte=date)
        discount = discounts.first()  # First or None
        prices = Price.objects.filter(Product=self, DateAdded__lte=date).order_by('-DateAdded')
        price = prices.first()  # First or None
        return price if discount is None else discount

    def get_price_table(self):
        return

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['SKU'], name='unique_Product')
        ]


class ProductInfo(models.Model):
    Product = models.ForeignKey(Product, on_delete=models.PROTECT)
    Language = models.ForeignKey(Language, on_delete=models.PROTECT)
    Name = models.CharField(max_length=255, blank=False, verbose_name=_('Product Name'),
                            help_text=_('Full product name with Series before name. No Category should be included.'))
    Tagline = models.CharField(max_length=255, blank=True, verbose_name=_('Tagline'),
                               help_text=_('A catchphrase or slogan that can make the product remembered.'))
    Specification = models.CharField(max_length=255, blank=True, verbose_name=_('Specification'),
                                     help_text=_('Specification for product: size, weight etc.'))
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
    Text = MarkdownxField(blank=True)
    TextQuality = models.IntegerField(choices=[
        (0, _('Not tested')),
        (1, _('Low quality')),
        (2, _('Medium quality')),
        (3, _('Good quality')),
    ], default=0)
    TimestampCreated = models.DateTimeField(auto_now_add=True)
    TimestampModified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.Product} / {self.Language} / {self.Order} / {self.Name}'

    @property
    def short_text(self):
        return truncatechars(self.Text, 100)

    @property
    def formatted_markdown(self):
        return markdownify(self.Text)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['Product', 'Language', 'Order'], name='unique_Tab')
        ]


class Price(models.Model):
    Product = models.ForeignKey(Product, on_delete=models.PROTECT)

    DateAdded = models.DateField(blank=True, null=True)
    Price = models.DecimalField(max_digits=10, decimal_places=2, blank=False)
    Currency = models.ForeignKey(Currency, on_delete=models.PROTECT)
    PV = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    GFT = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    Comment = models.CharField(max_length=255, blank=True)

    TimestampCreated = models.DateTimeField(auto_now_add=True)
    TimestampModified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.Product} / {self.Currency} / {self.DateAdded} / {self.Price} / {self.PV}'

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['Product', 'Currency', 'DateAdded'], name='unique_Price')
        ]


class Discount(models.Model):
    Product = models.ForeignKey(Product, on_delete=models.PROTECT)
    Action = models.ForeignKey(Action, on_delete=models.PROTECT, blank = True, null = True)

    DateStart = models.DateTimeField(blank=False, null=False)
    DateEnd = models.DateTimeField(blank=False, null=False)
    Price = models.DecimalField(max_digits=10, decimal_places=2, blank=False)
    Currency = models.ForeignKey(Currency, on_delete=models.PROTECT)
    PV = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    Comment = models.CharField(max_length=255, blank=True)

    TimestampCreated = models.DateTimeField(auto_now_add=True)
    TimestampModified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.Product} / {self.Currency} / {self.DateStart} / {self.Price} / {self.PV}'

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['Product', 'Currency', 'DateStart', 'DateEnd'], name='unique_Discount'),
            models.CheckConstraint(
                check=Q(DateEnd__gte=F("DateStart")),
                name='check_Discount_Dates_are_in_correct_order'
            )
        ]


class Image(models.Model):
    Product = models.ForeignKey(Product, on_delete=models.PROTECT)
    Image = models.ImageField(upload_to='products/')
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
    Product = models.ManyToManyField(Product, related_name='tags_of_product', blank=True)
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
