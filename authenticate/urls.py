from django.urls import path

from authenticate.views import AuthCreateView, ProfileUpdateView, district_view, LogoutView,PasswordUpdateView

urlpatterns = [
    path('auth/', AuthCreateView.as_view(), name='auth'),
    path('profile/', ProfileUpdateView.as_view(), name='profile'),
    path('district-list/', district_view, name='district-list'),
    path('profile/logout/', LogoutView.as_view(), name='logout'),
    path('profile/change-password/', PasswordUpdateView.as_view(), name='change-password'),

]


