import re

from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from django.forms import Form
from django.forms.fields import CharField
from django.utils.translation import gettext as _

from authenticate.models import User

class AuthForm(Form):
    phone_number = CharField ()
    password = CharField()

    def clean_phone_number(self):
        data = self.cleaned_data
        phone_number = data.get('phone_number')
        return re.sub('\D', '', phone_number)

    def clean_password(self):
        password = self.data.get('password')
        return make_password(password)

    def clean(self):
        data = self.cleaned_data
        password = data.get('password')
        phone_number = data.get('phone_number')
        query = User.objects.filter(phone_number=phone_number)
        if query.exists():
            user = query.first()
            if user.check_password(password):
                self.user = user
            else:
                raise ValidationError(_('Invalid password'))
        else:
            user = self.save()
            self.user = user

    def save(self):
        phone_number = self.cleaned_data.get('phone_number')
        user = User.objects.create(phone_number=phone_number)
        user.set_password(self.cleaned_data.get('password'))
        user.save()
        return user









