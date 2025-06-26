from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.db.models.aggregates import Count
from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import TemplateView, ListView, CreateView

from apps.forms import OrderForm
from apps.models import Category, Product, Order, WishList


# Create your views here.

class HomeListView(ListView):
    queryset = Category.objects.all()
    template_name = 'apps/home.html'
    context_object_name = 'categories'

    def get_context_data(self, *args, **kwargs):
        data = super().get_context_data(*args, **kwargs)
        data['products'] = Product.objects.all()
        return data


class ProductListView(ListView):
    queryset = Product.objects.all()
    template_name = 'apps/product-list.html'
    context_object_name = 'products'

    def get_queryset(self):
        category_slug =self.request.GET.get('category_slug')
        query = super().get_queryset()
        if category_slug:
            query = query.filter(category=Category.objects.get(slug=category_slug))
        return query

    def get_context_data(self, *args, **kwargs):
        data = super().get_context_data(*args, **kwargs)
        data['categories'] = Category.objects.all()
        data['c_slug'] = self.request.GET.get('category_slug')
        return data


class OqimTemplateView(TemplateView):
    template_name = 'apps/oqim.html'

class MarketListView(ListView):
    template_name = 'apps/market.html'
    queryset = Product.objects.all()
    context_object_name = 'products'

    def get_queryset(self):
        category_slug =self.request.GET.get('category_slug')
        query = super().get_queryset()
        if category_slug:
            query = query.filter(category__slug=category_slug)
        return query

    def get_context_data(self, *args, **kwargs):
        data = super().get_context_data(*args, **kwargs)
        data['categories'] = Category.objects.all()
        data['c_slug'] = self.request.GET.get('category_slug')
        return data


class OrderCreateView(CreateView):
    template_name = 'apps/order-form.html'
    queryset = Order.objects.all()
    context_object_name = 'order'
    form_class = OrderForm

    def get_context_data(self, **kwargs):
        product_id = self.kwargs.get('pk')
        data = super().get_context_data(**kwargs)
        data['product'] = Product.objects.get(id=product_id)
        return data

    def form_valid(self, form):
        order = form.save(commit=False)
        order['customer'] = self.request.user
        order = order.save()
        return render(self.request, 'apps/order-receive.html', {'order': order})

    def form_invalid(self, form):
        for message in form.errors.values():
            messages.error(self.request, message)
        return super().form_invalid(form)


class OrderListView(ListView):
    template_name = 'apps/order-list.html'
    queryset = Order.objects.all()
    context_object_name = 'orders'

    def get_queryset(self):
        query = super().get_queryset().filter(customer=self.request.user)
        return query


class SearchListView(ListView):
    queryset = Product.objects.all()
    context_object_name = 'products'
    template_name = 'apps/search.html'

    def get_queryset(self):
        search = self.request.GET.get('search')
        query = super().get_queryset().filter(Q(title__icontains=search) |
                                              Q(description__icontains=search) |
                                              Q(category__name__icontains=search))
        return query.distinct()

def wishlist_view(request, pk):
    query = WishList.objects.filter(product_id=pk, user = request.user)
    liked = False
    if not query.exists():
        liked = True
        WishList.objects.create(product_id=pk, user = request.user)
    else:
        liked = False
        query.delete()
    return JsonResponse({'liked': liked})

class WishListView(LoginRequiredMixin,ListView):
    queryset = WishList.objects.all()
    context_object_name = 'wishlists'
    template_name = 'apps/wishlist.html'

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    def get_context_data(self, *args, **kwargs):
        data = super().get_context_data(*args, **kwargs)
        data['total'] = WishList.objects.filter(user=self.request.user).aggregate(total=Count('id') )['total']
        return data



