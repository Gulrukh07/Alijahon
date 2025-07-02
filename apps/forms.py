from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django.utils.translation import gettext as _

from apps.models import Order, SiteStatics, Thread, Product, Withdrawal


class OrderForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ModelForm, self).__init__(*args, **kwargs)
        self.fields['total'].required = False
        self.fields['thread'].required = False

    class Meta:
        model = Order
        fields = 'fullname', 'phone_number', 'product', 'total', 'thread'

    def clean_total(self):
        product = self.cleaned_data['product']
        site = SiteStatics.objects.first()
        total_price = product.price + site.delivery_price
        thread_id = self.data.get('thread', None)
        if thread_id:
            thread = Thread.objects.get(id=thread_id)
            total_price -= thread.discount
        return total_price

class ThreadModelForm(ModelForm):
    class Meta:
        model = Thread
        fields = "name","discount", "product"

    def clean_discount(self):
        data = self.cleaned_data
        discount = self.cleaned_data.get("discount")
        product_id = self.data.get("product")
        product = Product.objects.get(id=product_id)

        if discount > product.seller_price:
            raise ValidationError(_("Discount exceeded the limit"))
        return discount

class WithdrawalModelForm(ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(ModelForm, self).__init__(*args, **kwargs)
        self.fields['user'].required = False

    class Meta:
        model = Withdrawal
        fields = "card_number", "amount", 'user'

    def clean_user(self):
        return self.user
    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        user = self.user
        if amount > user.balance:
            raise ValidationError(_("You don't have enough money"))
        return amount

