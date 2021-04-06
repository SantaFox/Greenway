from django.conf import settings
from django.db import models

from products.models import Product


class Account(models.Model):
    User = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    Name = models.CharField(max_length=50, blank=False)
    TimestampCreated = models.DateTimeField(auto_now_add=True)
    TimestampModified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.User} / {self.Name}'

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['User', 'Name'], name='unique_Account')
        ]


class Order(models.Model):
    User = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    Date = models.DateField(auto_now=True, blank=False)
    TimestampCreated = models.DateTimeField(auto_now_add=True)
    TimestampModified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.pk)


class OrderPosition(models.Model):
    Order = models.ForeignKey(Order, on_delete=models.PROTECT)
    Product = models.ForeignKey(Product, on_delete=models.PROTECT)
    Quantity = models.PositiveIntegerField(blank=False)
    Price = models.DecimalField(max_digits=10, decimal_places=2, blank=False)
    TimestampCreated = models.DateTimeField(auto_now_add=True)
    TimestampModified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.pk)

    # class Meta:
    #     constraints = [
    #         models.UniqueConstraint(fields=['Code'], name='unique_Order')
    #     ]