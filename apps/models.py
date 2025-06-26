from django.db import models
from django.db.models import Model, URLField, CASCADE, ForeignKey, ImageField, SET_NULL
from django.db.models.enums import TextChoices
from django.db.models.fields import CharField, DecimalField, IntegerField, TextField, DateTimeField, SlugField
from django.utils.text import slugify
from django.utils.translation import gettext as _


# Create your models here.

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
    description = TextField()
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
    # thread = ForeignKey('apps.Thread', on_delete=SET_NULL, null=True, blank=True, related_name='orders')

    def __str__(self):
        return self.fullname

class WishList(Model):
    user = ForeignKey('authenticate.User', on_delete=CASCADE, related_name='wishlists')
    product = ForeignKey('apps.Product', on_delete=CASCADE, related_name='wishlists')

    class Meta:
        unique_together = 'user', 'product'