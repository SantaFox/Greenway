from django.conf import settings
from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from products.models import Currency, Product


# https://gist.github.com/freewayz/69d1b8bcb3c225bea57bd70ee1e765f8

class ModelIsDeletableMixin(models.Model):

    def is_deletable(self):
        related_list = []
        # get all the related object
        for rel in self._meta.get_fields():
            try:
                # check if there is a relationship with at least one related object
                related = rel.related_model.objects.filter(**{rel.field.name: self})
                if related.exists():
                    related_list.append(related)
                    # if there is return a Tuple of flag = False the related_model object
            except AttributeError:  # an attribute error for field occurs when checking for AutoField
                pass  # just pass as we dont need to check for AutoField
        return related_list

    class Meta:
        abstract = True


class Account(ModelIsDeletableMixin, models.Model):
    User = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    Name = models.CharField(max_length=50, blank=False, verbose_name=_('Account Name'),
                            help_text=_('Account name that is easy to use and remember.'))

    TimestampCreated = models.DateTimeField(auto_now_add=True)
    TimestampModified = models.DateTimeField(auto_now=True)

    # Accounts intended to be multi-currency

    def __str__(self):
        return f'{self.User} / {self.Name}'

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['User', 'Name'], name='unique_Account')
        ]


class Counterparty(ModelIsDeletableMixin, models.Model):
    User = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    Name = models.CharField(max_length=50, blank=False, verbose_name=_('Counterparty Name'),
                                 help_text=_('Name of the Counterparty, preferably "Surname Name"'))

    Phone = models.CharField(max_length=50, blank=True)
    Email = models.CharField(max_length=50, blank=True)
    Telegram = models.CharField(max_length=50, blank=True)
    Instagram = models.CharField(max_length=50, blank=True)
    Facebook = models.CharField(max_length=50, blank=True)
    Address = models.CharField(max_length=255, blank=True)
    City = models.CharField(max_length=50, blank=True)
    Memo = models.TextField(blank=True)

    IsSupplier = models.BooleanField(default=False)
    IsCustomer = models.BooleanField(default=False)

    TimestampCreated = models.DateTimeField(auto_now_add=True)
    TimestampModified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.User} / {self.Name}'

    class Meta:
        verbose_name_plural = "Counterparties"
        constraints = [
            models.UniqueConstraint(fields=['User', 'Name'], name='unique_Counterparty'),
            models.CheckConstraint(
                check=Q(IsSupplier=True) | Q(IsCustomer=True),
                name='check_Counterparty_Supplier_or_Customer_is_Set'
            )
        ]


class Operation(models.Model):
    User = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    DateOperation = models.DateField(blank=False, verbose_name=_('Operation Date'),
                                     help_text=_('Date when this Operation was executed'))
    Type = models.IntegerField(choices=[
        (1, _('Customer Order')),
        (2, _('Supplier Order')),
        (3, _('Received Payment')),
        (4, _('Sent Payment')),
        (5, _('Delivered Goods')),
        (6, _('Received Goods')),
        (7, _('Deposited Money')),
        (8, _('Withdrawn money')),
        (9, _('Break set to items')),
    ], blank=False, null=True)

    # System block
    TimestampCreated = models.DateTimeField(auto_now_add=True)
    TimestampModified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.User} / {self.DateOperation} / {self.get_Type_display()}'


class SupplierOrder(Operation):
    Counterparty = models.ForeignKey(Counterparty, on_delete=models.PROTECT, blank=True, null=True)

    GreenwayOrderNum = models.CharField(max_length=10, blank=True)

    # Delivery-related block
    DatePlaced = models.DateField(blank=True, null=True)  # Date placed with supplier /
    DateDispatched = models.DateField(blank=True, null=True)  # Date dispatched by supplier / to customer
    DateDelivered = models.DateField(blank=True, null=True)  # Date received from supplier / by customer
    TrackingNumber = models.CharField(max_length=50, blank=True)
    CourierService = models.CharField(choices=[
        ('DHL', 'DHL Express'),
        ('Post', 'Ordinary Post'),
    ], max_length=10, blank=True, null=True)

    Amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    Currency = models.ForeignKey(Currency, on_delete=models.PROTECT, blank=True, null=True)
    GFT = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    PV = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    Memo = models.TextField(blank=True)

    def __str__(self):
        return f'{self.User} / {self.DateOperation} / {self.Counterparty}'

    class Meta:
        verbose_name_plural = "Supplier Orders"


class CustomerOrder(Operation):
    Counterparty = models.ForeignKey(Counterparty, on_delete=models.PROTECT, blank=True, null=True)

    DateDispatched = models.DateField(blank=True, null=True, verbose_name=_('Dispatch Date'),
                                      help_text=_(('Date when this Order was dispatched to the Customer.'
                                                   'Until then, the Order is prepared but held in Storage.')))
    DateDelivered = models.DateField(blank=True, null=True, verbose_name=_('Delivery Date'),
                                     help_text=_(('Date when this Order was delivered to the Customer. '
                                                  'In case of Detailed Delivery, the date of last delivery is used.')))
    TrackingNumber = models.CharField(max_length=50, blank=True, verbose_name=_('Tracking Number'),
                                      help_text=_('Tracking Number provided by used Courier Service.'))
    CourierService = models.CharField(choices=[
        ('DHL', 'DHL Express'),
        ('Post', 'Ordinary Post'),
    ], max_length=10, blank=True, null=True)

    DetailedDelivery = models.BooleanField(default=False, verbose_name=_('Detailed Delivery'),
                                           help_text=_('Delivery of each Position is managed separately'))

    Amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name=_('Amount'),
                                 help_text=_('Amount to be paid by Customer.'))
    Currency = models.ForeignKey(Currency, on_delete=models.PROTECT, blank=True, null=True, verbose_name=_('Currency'),
                                 help_text=_('Currency of Customer payment.'))

    Memo = models.TextField(blank=True, verbose_name=_('Memo'),
                            help_text=_('Memo related to this Customer Order'))

    def __str__(self):
        return f'{self.User} / {self.DateOperation} / {self.Counterparty}'

    class Meta:
        verbose_name_plural = "Customer Orders"


class ItemSetBreakdown(Operation):
    Product = models.ForeignKey(Product, on_delete=models.PROTECT, blank=True, null=True)
    Quantity = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        return f'{self.User} / {self.DateOperation} / {self.Product} / {self.Quantity}'

    class Meta:
        verbose_name_plural = "Item Set Breakdowns"


class OperationPosition(models.Model):
    Operation = models.ForeignKey(Operation, on_delete=models.PROTECT)

    Product = models.ForeignKey(Product, on_delete=models.PROTECT)
    Quantity = models.PositiveIntegerField(blank=False)

    TimestampCreated = models.DateTimeField(auto_now_add=True)
    TimestampModified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.Operation} / {self.Product} / {self.Quantity}'

    class Meta:
        verbose_name_plural = "Operation Positions"


class SupplierOrderPosition(OperationPosition):
    # Purchase options:
    # Money (normal or internal)
    Price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    Currency = models.ForeignKey(Currency, on_delete=models.PROTECT, blank=True, null=True)
    # or GFT
    GFT = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    # or Free because of temporary action
    FreeOnAction = models.BooleanField(default=False, blank=False)

    PV = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return f'{self.Operation} / {self.Product} / {self.Quantity} / {self.Price} / {self.Currency}'

    class Meta:
        verbose_name_plural = "Supplier Order Positions"


class CustomerOrderPosition(OperationPosition):
    Price = models.DecimalField(max_digits=10, decimal_places=2, blank=False)
    Currency = models.ForeignKey(Currency, on_delete=models.PROTECT)
    Discount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)  # Applied on Total
    DiscountReason = models.CharField(max_length=50, blank=True)

    CustomerOrderStatus = models.IntegerField(choices=[
        # Stock control table columns: In Stock | Reserved | To be Ordered | Incoming | Final
        (1, _('In stock / prepared for delivery')),  # Existing item is reserved
        (2, _('In stock / should be ordered')),  # Item exists and not reserved, but decided to be ordered
        (3, _('Not in stock / need to be ordered')),  # Missing item shows as TO BE ORDERED
        (4, _('Not in stock / waiting for incoming')),  # Missing item shows as INCOMING
        (5, _('Not in stock / no delivery control')),  # Missing item is... ?
        (6, _('Delivered to customer')),
    ], blank=True, null=True)
    DateDelivered = models.DateField(blank=True, null=True)  # Date received from supplier / by customer

    def __str__(self):
        return f'{self.Operation} / {self.Product} / {self.Quantity} / {self.Price} / {self.Currency}'

    class Meta:
        verbose_name_plural = "Customer Order Positions"


class ItemSetBreakdownPosition(OperationPosition):

    def __str__(self):
        return f'{self.Operation} / {self.Product}'

    class Meta:
        verbose_name_plural = "Item Set Breakdown Positions"


class Payment(Operation):
    DEBIT = 'D'
    CREDIT = 'C'
    TYPE_CHOICES = (
        (DEBIT, _('Debit')),
        (CREDIT, _('Credit')),
    )
    ParentOperation = models.ForeignKey(Operation, on_delete=models.PROTECT, related_name='Parent', blank=True,
                                        null=True)
    TransactionType = models.CharField(choices=TYPE_CHOICES, max_length=1, blank=False)

    Account = models.ForeignKey(Account, on_delete=models.PROTECT, blank=True, null=True)
    Amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    Currency = models.ForeignKey(Currency, on_delete=models.PROTECT, blank=True, null=True)

    def __str__(self):
        return f'{self.ParentOperation} / {self.TransactionType} / {self.Amount} / {self.Currency.Code}'
