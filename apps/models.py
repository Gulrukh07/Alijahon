from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.db.models import Model, URLField, CASCADE, ForeignKey, ImageField, SET_NULL
from django.db.models.enums import TextChoices
from django.db.models.fields import CharField, DecimalField, IntegerField, TextField, DateTimeField, SlugField, \
    DateField, BooleanField
from django.utils.text import slugify
from django.utils.translation import gettext as _


# Create your models here.t

class Category(Model):
    image = URLField()
    name = models.CharField(max_length=100)
    slug = SlugField()

    def save(self, *args, **kwargs):
        slug = slugify(self.name)  #
        i = 1
        while self.__class__.objects.filter(slug=slug).exists():
            slug += f"-{i}"
            i += 1
        self.slug = slug
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Product(Model):
    image = ImageField(upload_to='products/%Y/%m/%d')
    title = CharField(max_length=100)
    price = DecimalField(decimal_places=2, max_digits=10)
    category = ForeignKey(Category, on_delete=CASCADE, related_name='products')
    quantity = IntegerField(default=1)
    description = RichTextUploadingField()
    created = DateTimeField(auto_now_add=True)
    updated = DateTimeField(auto_now=True)
    seller_price = DecimalField(decimal_places=2, max_digits=10, null=True, blank=True )
    message = CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.title

class Order(Model):
    class OrderStatus(TextChoices):
        NEW = _('new'), _('New'),
        READY_TO_DELIVERY = _('ready_to_delivery'), _('Ready_to_delivery'),
        DELIVERING = _('delivering'), _('Delivering'),
        DELIVERED = _('delivered'), _('Delivered'),
        NOT_CONNECTED = _('not_connected'), _('Not Connected'),
        CANCELED = _('canceled'), _('Canceled'),
        ARCHIVED = _('archived'), _('Archived')

    customer = ForeignKey('authenticate.User', on_delete=SET_NULL, null=True, blank=True, related_name='orders')
    product = ForeignKey('apps.Product', on_delete=SET_NULL,null=True, blank=True, related_name='orders')
    quantity = IntegerField(default=1)
    created = DateTimeField(auto_now_add=True)
    status = CharField(max_length=20, choices=OrderStatus.choices, default=OrderStatus.NEW)
    fullname = CharField(max_length=255)
    phone_number = CharField(max_length=20)
    total = DecimalField(decimal_places=2, max_digits=10, null=True, blank=True)
    comment = TextField(null=True, blank=True)
    thread = ForeignKey('apps.Thread', on_delete=SET_NULL, null=True, blank=True, related_name='orders')
    updated = DateTimeField(auto_now=True, null=True, blank=True)
    operator = ForeignKey('authenticate.User', on_delete=SET_NULL, null=True, blank=True, related_name='operator_orders')
    deliver = ForeignKey('authenticate.User', on_delete=SET_NULL, null=True, blank=True, related_name='deliver_orders')
    delivered_date = DateField(null=True, blank=True)
    hold = BooleanField(default=False)
    district = ForeignKey('authenticate.District', on_delete=SET_NULL, null=True, blank=True, related_name='orders')

    def __str__(self):
        return self.fullname

class WishList(Model):
    user = ForeignKey('authenticate.User', on_delete=CASCADE, related_name='wishlists')
    product = ForeignKey('apps.Product', on_delete=CASCADE, related_name='wishlists')

    class Meta:
        unique_together = 'user', 'product'

class Thread(Model):
    owner = ForeignKey('authenticate.User', on_delete=CASCADE, related_name='threads')
    product = ForeignKey('apps.Product', on_delete=CASCADE, related_name='threads')
    discount = DecimalField(decimal_places=2, max_digits=10, null=True, blank=True)
    name = CharField(max_length=255)
    created = DateTimeField(auto_now_add=True)
    visit_count = IntegerField(default=0)

    @property
    def discount_amount(self):
        return self.product.price - self.discount

class SiteStatics(Model):
    delivery_price = DecimalField(decimal_places=2, max_digits=10, null=True, blank=True)
    giveaway_image = ImageField(upload_to='static/giveaway/%Y/%m/%d', null=True, blank=True)
    giveaway_start_time = DateField(null=True, blank=True)
    giveaway_end_time = DateField(null=True, blank=True)
    giveaway_description = RichTextUploadingField(null=True, blank=True)

class Withdrawal(Model):
    class WithdrawalStatus(TextChoices):
        UNDER_REVIEW = _('under review'), _('Under review'),
        COMPLETED = _('completed'), _('Completed'),
        CANCELED = _('canceled'), _('Canceled'),

    user = ForeignKey('authenticate.User', SET_NULL, null=True, blank=True, related_name='withdrawals')
    amount = DecimalField(decimal_places=0, max_digits=10)
    card_number = CharField(max_length=255)
    withdraw_date = DateField(auto_now_add=True)
    status = CharField(max_length=20, choices=WithdrawalStatus.choices, default=WithdrawalStatus.UNDER_REVIEW)
    pay_check = ImageField(upload_to='withdrawals/%Y/%m/%d', null=True, blank=True)
    comment = TextField(null=True, blank=True)
