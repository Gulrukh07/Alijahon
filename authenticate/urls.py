from django.urls import path

from authenticate.views import AuthCreateView, ProfileUpdateView, district_view, LogoutView, \
    PasswordFormView, telegram_login

urlpatterns = [
    path('auth/', AuthCreateView.as_view(), name='auth'),
    path("login/telegram", telegram_login, name="telegram_login"),

    path('profile/', ProfileUpdateView.as_view(), name='profile'),
    path('district-list/', district_view, name='district-list'),
    path('profile/logout/', LogoutView.as_view(), name='logout'),
    path('profile/change-password/', PasswordFormView.as_view(), name='change-password'),


]


