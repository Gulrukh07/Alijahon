from django.urls import path

from apps.views import HomeListView, ProductListView, MarketListView, OrderCreateView, OrderListView, \
    SearchListView, wishlist_view, WishListView, ThreadCreateView, ThreadListView, ThreadDetailView, StatisticsListView, \
    CategoryListView, GiveAwayListView

urlpatterns = [
    path('', HomeListView.as_view(), name='home'),
    path('product-list/', ProductListView.as_view(), name='product-list'),
    path('category', CategoryListView.as_view(), name='category-list'),
    path('search', SearchListView.as_view(), name='search'),
    path('giveaway', GiveAwayListView.as_view(), name='giveaway'),
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
# -------------- market /thread  -----------------
urlpatterns += [
    path('market/', MarketListView.as_view(), name='market'),
    path('thread/', ThreadListView.as_view(), name='thread-list'),
    path('thread-form', ThreadCreateView.as_view(), name='thread-form'),
    path('thread-detail/<int:pk>', ThreadDetailView.as_view(), name='thread-detail'),
    path('thread-statistics', StatisticsListView.as_view(), name='thread-statistics'),
]
