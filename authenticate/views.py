from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.hashers import check_password
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView, UpdateView

from authenticate.forms import AuthForm, ProfileForm, PasswordForm
from authenticate.models import User, Region, District


class AuthCreateView(FormView):
    template_name = 'auth/login.html'
    model = User
    form_class = AuthForm
    success_url = reverse_lazy('home')


    def form_valid(self, form):
        user = form.user
        login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')
        return super().form_valid(form)


    def form_invalid(self, form):
        for error in form.errors.items():
            messages.error(self.request, error[1])
        return super().form_invalid(form)


class ProfileUpdateView(LoginRequiredMixin,UpdateView):
    queryset = User.objects.all()
    form_class = ProfileForm
    template_name = 'auth/profile.html'
    success_url = reverse_lazy('home')
    context_object_name = 'user'

    def get_object(self, *args, **kwargs):
        return self.request.user

    def get_context_data(self):
        data = super().get_context_data()
        data['regions'] = Region.objects.all()
        return data

    def form_invalid(self, form):
        pass

def district_view(request):
    region_id = request.GET.get('region_id')
    districts = District.objects.filter(region_id=region_id).values("id", "name")
    data = [{"id": district.get('id'), "name": district.get("name")}for district in districts]
    return JsonResponse(data, safe=False)


class LogoutView(View):
    def get(self, request):
        logout(self.request)
        return redirect('auth')


class PasswordFormView(LoginRequiredMixin,FormView):
    template_name = 'auth/profile.html'
    form_class = PasswordForm
    success_url = reverse_lazy('profile')

    def form_valid(self, form):
        data = form.cleaned_data
        old_password = data.get('old_password')
        new_password = data.get('new_password')
        if check_password(old_password, self.request.user.password):
            user = self.request.user
            user.set_password(new_password)
            user.save()
            login(self.request, user)
            messages.success(self.request, 'Your password was successfully updated!')
            return redirect('auth')
        else:
            messages.error(self.request, 'Your password was not correct!')
            return redirect('profile')

    def form_invalid(self, form):
        for error in form.errors.values():
            messages.error(self.request, error[0])
        return super().form_invalid(form)



def telegram_login(request):
    phone_number = request.GET.get('phone_number')
    password = request.GET.get('password')
    query = User.objects.filter(phone_number=phone_number)
    if query.exists():
        user = query.first()
        if user.check_password(password):
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('home')
        else:
            messages.error(request, 'Invalid password!')
            return redirect('auth')
    else:
        user = User.objects.create(phone_number=phone_number, password=password)
        user.set_password(password)
        user.save()
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        return redirect('home')












