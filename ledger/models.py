from django.conf import settings
from django.db import models
from django.db.models import Q, Sum, Count
from django.utils.translation import gettext_lazy as _

from model_utils.managers import InheritanceManager

from products.models import Currency, Product, Price

DEBIT = 'D'
CREDIT = 'C'
TYPE_CHOICES = (
    (DEBIT, _('Debit')),
    (CREDIT, _('Credit')),
)

POSTAL_CHOICES = (
    ('DHL', 'DHL Express'),
    ('AKIS', 'Akis Express'),
    ('CZP', 'Czech Post'),
    ('POST', 'Ordinary Post'),
    ('GLS', 'GLS Post Service')
)


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
        verbose_name_plural = _('Accounts')
        constraints = [
            models.UniqueConstraint(fields=['User', 'Name'], name='unique_Account')
        ]


class Counterparty(ModelIsDeletableMixin, models.Model):
    User = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    Name = models.CharField(max_length=50, blank=False, verbose_name=_('Counterparty Name'),
                            help_text=_('Name of the Counterparty, preferably "Surname Name"'))

    Phone = models.CharField(max_length=50, blank=True, verbose_name=_('Contact Phone'),
                             help_text=_('Name of the Counterparty, preferably "Surname Name"'))
    Email = models.CharField(max_length=50, blank=True, verbose_name=_('Email address'),
                             help_text=_('Name of the Counterparty, preferably "Surname Name"'))
    Telegram = models.CharField(max_length=50, blank=True, verbose_name=_('Telegram'),
                                help_text=_('Telegram profile name'))
    Instagram = models.CharField(max_length=50, blank=True, verbose_name=_('Instagram'),
                                 help_text=_('Name of the Counterparty, preferably "Surname Name"'))
    Facebook = models.CharField(max_length=50, blank=True, verbose_name=_('Facebook'),
                                help_text=_('Name used in Facebook and Facebook Messenger'))
    Address = models.CharField(max_length=255, blank=True, verbose_name=_('Address'),
                               help_text=_('Address (without city)'))
    City = models.CharField(max_length=50, blank=True, verbose_name=_('City Name'),
                            help_text=_('City name only'))
    Memo = models.TextField(blank=True, verbose_name=_('Memo'),
                            help_text=_('Name of the Counterparty, preferably "Surname Name"'))

    IsSupplier = models.BooleanField(default=False, verbose_name=_('Act as Supplier'),
                                     help_text=_('Counterparty act as Supplier and can be selected in Supplier Order'))
    IsCustomer = models.BooleanField(default=False, verbose_name=_('Act as Customer'),
                                     help_text=_('Counterparty act as Customer and can be selected in Customer Order'))

    TimestampCreated = models.DateTimeField(auto_now_add=True)
    TimestampModified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.User} / {self.Name}'

    class Meta:
        verbose_name_plural = _("Counterparties")
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

    # System block
    TimestampCreated = models.DateTimeField(auto_now_add=True)
    TimestampModified = models.DateTimeField(auto_now=True)

    objects = InheritanceManager()

    def __str__(self):
        return f'{self.User} / {self.DateOperation}'


class SupplierOrder(ModelIsDeletableMixin, Operation):
    Counterparty = models.ForeignKey(Counterparty, on_delete=models.PROTECT, blank=True, null=True,
                                     verbose_name=_('Supplier Name'),
                                     help_text=_('Registered Supplier'))

    GreenwayOrderNum = models.CharField(max_length=10, blank=True, verbose_name=_('Supplier Order Num'),
                                        help_text=_('Number of this Order in the Supplier''s system'))

    # Delivery-related block
    DatePlaced = models.DateField(blank=True, null=True, verbose_name=_('Placement Date'),
                                  help_text=_('Date when this Order was placed to the Supplier system'))
    DateDispatched = models.DateField(blank=True, null=True, verbose_name=_('Dispatch Date'),
                                      help_text=_('Date when this Order was dispatched from the Supplier'))
    DateDelivered = models.DateField(blank=True, null=True, verbose_name=_('Delivery Date'),
                                     help_text=_('Date when this Order was delivered from the Supplier to Storage'))
    TrackingNumber = models.CharField(max_length=50, blank=True, verbose_name=_('Tracking Number'),
                                      help_text=_('Tracking Number provided by used Courier Service'))
    CourierService = models.CharField(choices=POSTAL_CHOICES, max_length=10, blank=True, null=True,
                                      verbose_name=_('Courier Service Name'),
                                      help_text=_('Select one from provided Courier Services'))
    DeliveryPrice = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True,
                                        verbose_name=_('Delivery price'),
                                        help_text=_('Price of delivery in the same currency as Amount, if separately \
                                        provided by the Supplier. Included in total Amount.'))

    Amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name=_('Amount'),
                                 help_text=_('Amount to be paid to the Supplier'))
    Currency = models.ForeignKey(Currency, on_delete=models.PROTECT, blank=True, null=True, verbose_name=_('Currency'),
                                 help_text=_('Currency of Supplier payment'))
    GFT = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name=_('GFT Amount'),
                              help_text=_('Gift value calculated in GFT (obsolete since 07.07.2021)'))
    Gift = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name=_('Gift Amount'),
                               help_text=_('Gift value calculated in payment Currency (actual since 07.07.2021)'))
    PV = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name=_('PV'),
                             help_text=_('Volume (PV) obtained from this Order'))

    Memo = models.TextField(blank=True, verbose_name=_('Memo'),
                            help_text=_('Memo related to this Supplier Order'))

    @property
    def get_paid_amount(self):
        amount_queryset = Payment.objects.filter(ParentOperation=self).aggregate(TotalAmount=Sum('Amount'))
        amount = amount_queryset['TotalAmount']
        return 0 if amount is None else amount

    @property
    def get_positions_count(self):
        pos_queryset = SupplierOrderPosition.objects.filter(Operation=self).aggregate(PositionCount=Count('id'))
        pos_count = pos_queryset['PositionCount']
        return 0 if pos_count is None else pos_count

    @property
    def get_payments_count(self):
        payments_queryset = Payment.objects.filter(ParentOperation=self).aggregate(PaymentCount=Count('id'))
        payments_count = payments_queryset['PaymentCount']
        return 0 if payments_count is None else payments_count

    def __str__(self):
        return f'{self.User} / {self.DateOperation} / {self.Counterparty} / {self.Amount} / {self.Currency}'

    class Meta:
        verbose_name_plural = _('Supplier Orders')


class CustomerOrder(ModelIsDeletableMixin, Operation):
    Customer = models.ForeignKey(Counterparty, on_delete=models.PROTECT, blank=True, null=True,
                                 verbose_name=_('Customer Name'),
                                 help_text=_('Registered Customer'))

    DateDispatched = models.DateField(blank=True, null=True, verbose_name=_('Dispatch Date'),
                                      help_text=_('Date when this Order was dispatched to the Customer. Until then,\
                                                   the Order is prepared but held in Storage'))
    DateDelivered = models.DateField(blank=True, null=True, verbose_name=_('Delivery Date'),
                                     help_text=_('Date when this Order was delivered to the Customer.\
                                                  In case of Detailed Delivery, the date of last delivery is used'))
    TrackingNumber = models.CharField(max_length=50, blank=True, verbose_name=_('Tracking Number'),
                                      help_text=_('Tracking Number provided by used Courier Service'))
    CourierService = models.CharField(choices=POSTAL_CHOICES, max_length=10, blank=True, null=True,
                                      verbose_name=_('Courier Service Name'),
                                      help_text=_('Select one from provided Courier Services'))
    DeliveryPrice = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True,
                                        verbose_name=_('Delivery price'),
                                        help_text=_('Price of delivery in the same currency as Amount, if Customer \
                                        is charged for it. Included in total Amount.'))

    DetailedDelivery = models.BooleanField(default=False, verbose_name=_('Detailed Delivery'),
                                           help_text=_('Delivery of each Position is managed separately'))

    Amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name=_('Amount'),
                                 help_text=_('Amount to be paid by Customer'))
    Currency = models.ForeignKey(Currency, on_delete=models.PROTECT, blank=True, null=True, verbose_name=_('Currency'),
                                 help_text=_('Currency of Customer payment'))

    Memo = models.TextField(blank=True, verbose_name=_('Memo'),
                            help_text=_('Memo related to this Customer Order'))

    @property
    def get_paid_amount(self):
        amount_queryset = Payment.objects.filter(ParentOperation=self).aggregate(TotalAmount=Sum('Amount'))
        amount = amount_queryset['TotalAmount']
        return 0 if amount is None else amount

    @property
    def get_positions_count(self):
        pos_queryset = CustomerOrderPosition.objects.filter(Operation=self).aggregate(PositionCount=Count('id'))
        pos_count = pos_queryset['PositionCount']
        return 0 if pos_count is None else pos_count

    @property
    def get_payments_count(self):
        payments_queryset = Payment.objects.filter(ParentOperation=self).aggregate(PaymentCount=Count('id'))
        payments_count = payments_queryset['PaymentCount']
        return 0 if payments_count is None else payments_count

    def __str__(self):
        return f'{self.User} / {self.DateOperation} / {self.Customer} / {self.Amount} / {self.Currency}'

    class Meta:
        verbose_name_plural = _('Customer Orders')


class ItemSetBreakdown(ModelIsDeletableMixin, Operation):
    Product = models.ForeignKey(Product, on_delete=models.PROTECT, blank=True, null=True)
    Quantity = models.PositiveIntegerField(blank=True, null=True)

    Memo = models.TextField(blank=True, verbose_name=_('Memo'),
                            help_text=_('Memo related to this ItemSet Breakdown'))

    def __str__(self):
        return f'{self.User} / {self.DateOperation} / {self.Product} / {self.Quantity}'

    class Meta:
        verbose_name_plural = _('Item Set Breakdowns')


class OperationPosition(models.Model):
    Operation = models.ForeignKey(Operation, on_delete=models.PROTECT)

    Product = models.ForeignKey(Product, on_delete=models.PROTECT, verbose_name=_('Product'),
                                help_text=_('Product'))
    Quantity = models.PositiveIntegerField(blank=False, verbose_name=_('Quantity'),
                                           help_text=_('Quantity of Products'))

    TimestampCreated = models.DateTimeField(auto_now_add=True)
    TimestampModified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.Operation} / {self.Product} / {self.Quantity}'

    @property
    def get_actual_price(self):
        prices = Price.objects.filter(Product=self.Product, DateAdded__lte=self.Operation.DateOperation).order_by('-DateAdded')
        price = prices.first()  # First or None
        return price.Price

    class Meta:
        verbose_name_plural = "Operation Positions"


class SupplierOrderPosition(OperationPosition):
    # Purchase options:
    # Money (normal or internal)
    Price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name=_('Price'),
                                help_text=_('Paid price per one Product'))
    Currency = models.ForeignKey(Currency, on_delete=models.PROTECT, blank=True, null=True, verbose_name=_('Currency'),
                                 help_text=_('Currency of the paid price'))
    # or GFT
    GFT = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    # or Free because of temporary action
    FreeOnAction = models.BooleanField(default=False, blank=False, verbose_name=_('Free Item'),
                                       help_text=_('This Position is free because of ongoing Action'))
    # or Price/Currency paid from Gift Account
    GiftPosition = models.BooleanField(default=False, blank=False, verbose_name=_('Gift'),
                                       help_text=_('This Position is purchased from accrued Gift funds'))

    PV = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name=_('PV'),
                             help_text=_('Volume (PV) obtained per one Product'))

    def __str__(self):
        return f'{self.Operation} / {self.Product} / {self.Quantity} / {self.Price} / {self.Currency}'

    class Meta:
        verbose_name_plural = "Supplier Order Positions"


class CustomerOrderPosition(OperationPosition):
    Price = models.DecimalField(max_digits=10, decimal_places=2, blank=False, verbose_name=_('Price'),
                                help_text=_('Sell price per one Product'))
    Currency = models.ForeignKey(Currency, on_delete=models.PROTECT, verbose_name=_('Currency'),
                                 help_text=_('Currency of the sell price'))
    Discount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name=_('Discount'),
                                   help_text=_('Discount applied to total amount for the position'))
    DiscountReason = models.CharField(max_length=50, blank=True, verbose_name=_('Discount Reason'),
                                      help_text=_('Reason for provision of Discount'))

    Status = models.IntegerField(choices=[
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
    TransactionType = models.CharField(choices=TYPE_CHOICES, max_length=1, blank=False)

    def __str__(self):
        return f'{self.Operation} / {self.Product}'

    class Meta:
        verbose_name_plural = "Item Set Breakdown Positions"


class Payment(ModelIsDeletableMixin, Operation):
    ParentOperation = models.ForeignKey(Operation, on_delete=models.PROTECT, related_name='Parent')
    TransactionType = models.CharField(choices=TYPE_CHOICES, max_length=1, blank=False)

    Account = models.ForeignKey(Account, on_delete=models.PROTECT, blank=False)
    Amount = models.DecimalField(max_digits=10, decimal_places=2, blank=False)
    Currency = models.ForeignKey(Currency, on_delete=models.PROTECT, blank=False)

    def __str__(self):
        return f'{self.ParentOperation} / {self.TransactionType} / {self.Amount} / {self.Currency.Code}'

    class Meta:
        verbose_name_plural = _("Payments")


class Transfer(ModelIsDeletableMixin, Operation):
    DebitAccount = models.ForeignKey(Account, on_delete=models.PROTECT, blank=True, null=True, related_name='debit_account')
    DebitAmount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    DebitCurrency = models.ForeignKey(Currency, on_delete=models.PROTECT, blank=True, null=True, related_name='debit_currency')

    CreditAccount = models.ForeignKey(Account, on_delete=models.PROTECT, blank=True, null=True, related_name='credit_account')
    CreditAmount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    CreditCurrency = models.ForeignKey(Currency, on_delete=models.PROTECT, blank=True, null=True, related_name='credit_currency')

    Memo = models.TextField(blank=True, verbose_name=_('Memo'),
                            help_text=_('Memo related to this Cash Transfer'))

    def __str__(self):
        return f'{self.User} / {self.DateOperation}'

    class Meta:
        verbose_name_plural = _("Cash Transfers")