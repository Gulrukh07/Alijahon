from django.contrib import messages
from django.contrib.auth import login
from django.urls import reverse_lazy
from django.views.generic import  CreateView

from authenticate.forms import AuthForm
from authenticate.models import User


class AuthCreateView(CreateView):
    template_name = 'auth/login.html'
    model = User
    form_class = AuthForm
    success_url = reverse_lazy('product-list')


    def form_valid(self, form):
        user = form.user
        login(self.request, user)
        return super().form_valid(form)


    def form_invalid(self, form):
        for error in form.errors.items():
            messages.error(self.request, error[1])
        return super().form_invalid(form)




