from django.forms import ModelForm

from apps.models import Order


class OrderForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ModelForm, self).__init__(*args, **kwargs)
        self.fields['total'].required = False

    class Meta:
        model = Order
        fields = 'fullname', 'phone_number', 'product', 'total'

    def clean_total(self):
        product = self.cleaned_data['product']
        return product.price


