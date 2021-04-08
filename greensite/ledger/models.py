from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from products.models import Currency, Product


class Account(models.Model):
    User = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    Name = models.CharField(max_length=50, blank=False)
    TimestampCreated = models.DateTimeField(auto_now_add=True)
    TimestampModified = models.DateTimeField(auto_now=True)
    # Accounts intended to be multi-currency

    def __str__(self):
        return f'{self.User} / {self.Name}'

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['User', 'Name'], name='unique_Account')
        ]


class Counterparty(models.Model):
    User = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    Name = models.CharField(max_length=50, blank=False)
    Phone = models.CharField(max_length=50, blank=True)
    Email = models.CharField(max_length=50, blank=True)
    Telegram = models.CharField(max_length=50, blank=True)
    Facebook = models.CharField(max_length=50, blank=True)
    Address = models.CharField(max_length=255, blank=True)
    Memo = models.TextField(blank=True)
    IsSupplier = models.BooleanField(default=False)
    IsCustomer = models.BooleanField(default=False)
    TimestampCreated = models.DateTimeField(auto_now_add=True)
    TimestampModified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.Name}'

    class Meta:
        verbose_name_plural = "Counterparties"
        constraints = [
            models.UniqueConstraint(fields=['User', 'Name'], name='unique_Counterparty')
        ]


class Operation(models.Model):
    User = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    DateOperation = models.DateField(blank=False)
    Type = models.IntegerField(choices=[
        (1, _('Customer Order')),
        (2, _('Supply Order')),
        (3, _('Received Payment')),
        (4, _('Sent Payment')),
        (5, _('Delivered Goods')),
        (6, _('Received Goods')),
        (7, _('Deposited Money')),
        (8, _('Withdrawn money')),
        (9, _('Break set to items')),
    ], blank=False, null=True)
    Counterparty = models.ForeignKey(Counterparty, on_delete=models.PROTECT)

    # Delivery-related block
    DatePlaced = models.DateField(blank=True, null=True)            # Date placed with supplier /
    DateDispatched = models.DateField(blank=True, null=True)        # Date dispatched by supplier / to customer
    DateDelivered = models.DateField(blank=True, null=True)         # Date received from supplier / by customer
    TrackingNumber = models.CharField(max_length=50, blank=True)

    # System block
    TimestampCreated = models.DateTimeField(auto_now_add=True)
    TimestampModified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.User} / {self.DateOperation } / {self.Counterparty} / {self.get_Type_display()}'


class OperationPosition(models.Model):
    Operation = models.ForeignKey(Operation, on_delete=models.PROTECT)
    Product = models.ForeignKey(Product, on_delete=models.PROTECT)
    Quantity = models.PositiveIntegerField(blank=False)
    Price = models.DecimalField(max_digits=10, decimal_places=2, blank=False)
    Currency = models.ForeignKey(Currency, on_delete=models.PROTECT)
    CustomerOrderStatus = models.IntegerField(choices=[
        # Stock control table columns: In Stock | Reserved | To be Ordered | Incoming | Final
        (1, _('In stock / prepared for delivery')),         # Existing item is reserved
        (2, _('In stock / should be ordered')),             # Item exists and not reserved, but decided to be ordered
        (3, _('Not in stock / need to be ordered')),        # Missing item shows as TO BE ORDERED
        (4, _('Not in stock / waiting for incoming')),      # Missing item shows as INCOMING
        (5, _('Not in stock / no delivery control')),       # Missing item is... ?
        (6, _('Delivered to customer')),
    ], blank=False, null=True)
    TimestampCreated = models.DateTimeField(auto_now_add=True)
    TimestampModified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.Operation} / {self.Product} / {self.Quantity} / {self.Price} / {self.Currency}'

    # class Meta:
    #     constraints = [
    #         models.UniqueConstraint(fields=['Code'], name='unique_Order')
    #     ]


class OperationAtom(models.Model):
    Operation = models.ForeignKey(Operation, on_delete=models.PROTECT)
    TimestampCreated = models.DateTimeField(auto_now_add=True)
    TimestampModified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.pk)