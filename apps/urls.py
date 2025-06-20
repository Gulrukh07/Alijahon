from django.conf.urls.i18n import i18n_patterns
from django.urls import path, include

from apps.views import HomeListView, ProductListView

urlpatterns = [
    path('', HomeListView.as_view(), name='home'),
    path('product-list/', ProductListView.as_view(), name='product-list'),
]

