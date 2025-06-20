from django.urls import path

from authenticate.views import AuthCreateView

urlpatterns = [
    path('auth/', AuthCreateView.as_view(), name='auth'),

]


