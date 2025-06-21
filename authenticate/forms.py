import re

from django.contrib.auth.hashers import make_password, check_password
from django.core.exceptions import ValidationError
from django.forms import Form
from django.forms.fields import CharField
from django.forms.models import ModelForm
from django.utils.translation import gettext as _

from authenticate.models import User

class AuthForm(Form):
    phone_number = CharField ()
    password = CharField()

    def clean_phone_number(self):
        data = self.cleaned_data
        phone_number = data.get('phone_number')
        return re.sub('\D', '', phone_number)

    def clean(self):
        data = self.cleaned_data
        password = data.get('password')
        phone_number = data.get('phone_number')
        query = User.objects.filter(phone_number=phone_number)
        if query.exists():
            user = query.first()
            if check_password(password, user.password):
                self.user = user
            else:
                raise ValidationError(_('Invalid password'))
        else:
            user = self.save()
            self.user = user
        return data

    def save(self):
        data = self.cleaned_data
        password = data.get('password')
        phone_number = data.get('phone_number')
        user = User.objects.create(phone_number=phone_number)
        user.set_password(password)
        user.save()
        return user


class ProfileForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ModelForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = False

    class Meta:
        model = User
        fields = 'first_name', 'last_name', 'address', 'about', 'telegram_id','district'











