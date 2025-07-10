import datetime
import re

from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django.utils.translation import gettext as _

from apps.models import Order, SiteStatics, Thread, Product, Withdrawal
from authenticate.models import User


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
        if amount <= 0:
            raise ValidationError(_("Amount cannot be negative"))
        if amount > user.balance:
            raise ValidationError(_("You don't have enough money"))
        return amount

    def clean_card_number(self):
        card_number = self.cleaned_data.get('card_number')
        pattern = r'^[1-9][0-9]{10}$'
        card_number = re.sub(pattern, '', card_number)
        return card_number

class OrderUpdateModelForm(ModelForm):
    def __init__(self, *args, **kwargs):
        self.order = kwargs.pop('order', None)
        self.employee = kwargs.pop('employee', None)
        super(ModelForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = False

    class Meta:
        model = Order
        fields = 'quantity' , 'delivered_date' , 'status' , 'comment' , 'district' , 'operator', 'deliver'

    def clean_operator(self):
        if self.employee.role == User.UserRoles.OPERATOR:
            return self.employee

    def clean_deliver(self):
        if self.employee.role == User.UserRoles.DELIVERER:
            return self.employee

    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')
        site = SiteStatics.objects.first()
        order = self.order


        if quantity > order.product.quantity:
            raise ValidationError(_("The product quantity cannot be greater than the product quantity"))
        if quantity <= 0:
            raise ValidationError(_("The product quantity cannot be negative"))
        if order.thread:
            order.total = order.thread.discount_amount * quantity + site.delivery_price
        else:
            order.total = order.product.price * quantity + site.delivery_price
        order.save()
        return quantity

    def clean_delivered_date(self):
        delivered_date = self.cleaned_data.get('delivered_date')
        now = datetime.date.today()
        if delivered_date and delivered_date < now:
            raise ValidationError(_("The delivered date cannot be less than the current date"))
        return delivered_date



