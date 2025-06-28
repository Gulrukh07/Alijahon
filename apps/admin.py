from django.contrib import admin

from apps.models import Category, Product, Order, SiteStatics


# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass

@admin.register(SiteStatics)
class SiteStatics(admin.ModelAdmin):
    pass

