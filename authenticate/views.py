from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView, UpdateView

from authenticate.forms import AuthForm, ProfileForm
from authenticate.models import User, Region, District


class AuthCreateView(FormView):
    template_name = 'auth/login.html'
    model = User
    form_class = AuthForm
    success_url = reverse_lazy('home')


    def form_valid(self, form):
        user = form.user
        login(self.request, user)
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






