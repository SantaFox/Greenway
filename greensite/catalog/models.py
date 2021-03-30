from django.db import models


# System classes below
class Language(models.Model):
    Code = models.CharField(max_length=3)
    # ISO = models.IntegerField()

    def __str__(self):
        return self.Code


class Currency(models.Model):
    Code = models.CharField(max_length=3)
    # ISO = models.IntegerField()

    def __str__(self):
        return self.Code


# Data classes below
class Product(models.Model):
    SKU = models.CharField(max_length=50, blank=False)
    DateAdded = models.DateField(blank=True, null=True)
    DateRemoved = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.SKU


class ProductInfo(models.Model):
    Product = models.ForeignKey(Product, on_delete=models.PROTECT)
    Language = models.ForeignKey(Language, on_delete=models.PROTECT)
    Name = models.CharField(max_length=255, blank=False)
    Specification = models.CharField(max_length=255, blank=True)
    TimestampCreated = models.DateTimeField(auto_now_add=True)
    TimestampModified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.Product} / {self.Language} / {self.Name}'


class Tab(models.Model):
    Product = models.ForeignKey(Product, on_delete=models.PROTECT)
    Language = models.ForeignKey(Language, on_delete=models.PROTECT)
    Order = models.IntegerField(blank=False)
    Name = models.CharField(max_length=255, blank=False)
    Text = models.TextField(blank=True)
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
