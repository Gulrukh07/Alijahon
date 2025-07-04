from django.urls import path

from apps.views import HomeListView, ProductListView, MarketListView, OrderCreateView, OrderListView, \
    SearchListView, wishlist_view, WishListView, ThreadCreateView, ThreadListView, ThreadDetailView, StatisticsListView, \
    CategoryListView, GiveAwayListView, WithdrawalCreateView, OperatorOrderListView, OrderUpdateView, \
    diagram_statistic_view, DiagramTemplateView

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
#--------------------------- withdraw  ----------------------------------
urlpatterns += [
    path('withdraw/', WithdrawalCreateView.as_view(), name='withdraw-form'),
]

#--------------------------- operator  ----------------------------------
urlpatterns += [
    path('operator-page/', OperatorOrderListView.as_view(), name='operator-page'),
    path('order-update/<int:pk>', OrderUpdateView.as_view(), name='order-update'),
]
urlpatterns += [
    path('diagram/', DiagramTemplateView.as_view(), name='diagram'),
    path('diagram-statistic', diagram_statistic_view, name='diagram-statistic'),
]
