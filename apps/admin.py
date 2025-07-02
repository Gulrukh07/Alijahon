from django.contrib import admin

from apps.models import Category, Product, SiteStatics, Withdrawal


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
@admin.register(Withdrawal)
class WithdrawalAdmin(admin.ModelAdmin):
    list_display = ("user", "amount", "card_number", "pay_check", "status")

    def save_model(self, request, obj, form, change):
        if obj.status == Withdrawal.WithdrawalStatus.UNDER_REVIEW:
            user = obj.user
            user.balance += obj.amount
            user.save()
        obj.save()

