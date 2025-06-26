from django.urls import path

from apps.views import HomeListView, ProductListView, MarketListView, OqimTemplateView, OrderCreateView, OrderListView,SearchListView, wishlist_view, WishListView

urlpatterns = [
    path('', HomeListView.as_view(), name='home'),
    path('product-list/', ProductListView.as_view(), name='product-list'),
    path('search', SearchListView.as_view(), name='search'),
]
#------------------   order   ------------
urlpatterns += [
    path('order-form/<int:pk>', OrderCreateView.as_view(), name='order-form'),
    path('order-list', OrderListView.as_view(), name='order-list'),
]

# -------------- user wishlist   -----------------
urlpatterns += [
    path('wishlist/<int:pk>', wishlist_view, name='wish'),
    path('liked-products', WishListView.as_view(), name='wishlist'),
]
# -------------- market   -----------------
urlpatterns += [
    path('market/', MarketListView.as_view(), name='market'),
]
# --------------   thread   -----------------
urlpatterns += [
    path('thread/', OqimTemplateView.as_view(), name='thread'),
]
