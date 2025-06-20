from django.db import models
from django.db.models import Model, URLField, CASCADE, ForeignKey, ImageField
from django.db.models.fields import CharField, DecimalField, IntegerField, TextField, DateTimeField, SlugField
from django.utils.text import slugify


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

    def __str__(self):
        return self.title
