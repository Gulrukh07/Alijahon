from datetime import datetime, timedelta

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, Sum, Count
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, TemplateView

from apps.forms import OrderForm, ThreadModelForm, WithdrawalModelForm, OrderUpdateModelForm
from apps.models import Category, Product, Order, WishList, Thread, SiteStatics, Withdrawal
from authenticate.models import User, Region


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
        category_slug = self.request.GET.get('category_slug')
        query = super().get_queryset()
        if category_slug:
            query = query.filter(category=Category.objects.get(slug=category_slug))
        return query

    def get_context_data(self, *args, **kwargs):
        data = super().get_context_data(*args, **kwargs)
        data['categories'] = Category.objects.all()
        data['c_slug'] = self.request.GET.get('category_slug')
        return data


class CategoryListView(ListView):
    queryset = Category.objects.all()
    template_name = 'apps/product-list.html'
    context_object_name = 'categories'


class MarketListView(ListView):
    template_name = 'apps/market/market.html'
    queryset = Product.objects.all()
    context_object_name = 'products'

    def get_queryset(self):
        category_slug = self.request.GET.get('category_slug')
        query = super().get_queryset()
        if category_slug == 'top':
            query = query.annotate(order_count=Count('orders')).order_by('-order_count')
        elif category_slug:
            query = query.filter(category__slug=category_slug)
        return query

    def get_context_data(self, *args, **kwargs):
        data = super().get_context_data(*args, **kwargs)
        data['categories'] = Category.objects.all()
        data['c_slug'] = self.request.GET.get('category_slug')
        return data


class OrderCreateView(LoginRequiredMixin, CreateView):
    template_name = 'apps/order/order-form.html'
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
        order.customer = self.request.user
        order.save()
        site = SiteStatics.objects.first()
        return render(self.request, 'apps/order/order-receive.html', {'order': order, 'site': site})

    def form_invalid(self, form):
        for message in form.errors.values():
            messages.error(self.request, message)
        return super().form_invalid(form)


class OrderListView(ListView):
    template_name = 'apps/order/order-list.html'
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
    query = WishList.objects.filter(product_id=pk, user=request.user)
    liked = False
    if not query.exists():
        liked = True
        WishList.objects.create(product_id=pk, user=request.user)
    else:
        liked = False
        query.delete()
    return JsonResponse({'liked': liked})


class WishListView(LoginRequiredMixin, ListView):
    queryset = WishList.objects.all()
    context_object_name = 'wishlists'
    template_name = 'apps/wishlist.html'

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    def get_context_data(self, *args, **kwargs):
        data = super().get_context_data(*args, **kwargs)
        data['total'] = WishList.objects.filter(user=self.request.user).aggregate(total=Count('id'))['total']
        return data


class ThreadCreateView(CreateView):
    queryset = Thread.objects.all()
    template_name = 'apps/market/market.html'
    form_class = ThreadModelForm
    success_url = reverse_lazy("thread-list")

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['products'] = Product.objects.all()
        data['categories'] = Category.objects.all()
        return data

    def form_valid(self, form):
        thread = form.save(commit=False)
        thread.owner = self.request.user
        thread.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        for message in form.errors.values():
            messages.error(self.request, message)
        return super().form_invalid(form)


class ThreadListView(ListView):
    queryset = Thread.objects.all().order_by('-created')
    template_name = 'apps/market/thread-list.html'
    context_object_name = 'threads'

    def get_queryset(self):
        query = super().get_queryset().filter(owner=self.request.user)
        return query


class ThreadDetailView(DetailView):
    queryset = Thread.objects.all()
    pk_url_kwarg = 'pk'
    template_name = 'apps/order/order-form.html'
    context_object_name = 'thread'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        thread = data.get('thread')
        thread.visit_count += 1
        thread.save()
        data['product'] = self.object.product
        return data


class StatisticsListView(ListView):
    queryset = Thread.objects.all()
    template_name = 'apps/market/statistics.html'
    context_object_name = 'threads'

    def get_queryset(self):
        period = self.request.GET.get('period')

        now = datetime.now()
        today_start = datetime(now.year, now.month, now.day, 0, 0, 0)
        today_end = datetime(now.year, now.month, now.day, 23, 59, 59)

        # Yesterday
        yesterday_start = today_start - timedelta(days=1)
        yesterday_end = today_end - timedelta(days=1)

        # Weekly
        week_start = today_start - timedelta(days=6)  # Including today, so 7 days total
        week_end = today_end

        # Monthly (30 kunlik)
        month_start = today_start - timedelta(days=29)
        month_end = today_end

        # All time
        all_start = datetime(2000, 1, 1, 0, 0, 0)
        all_end = today_end

        datetime_map = {
            "today": [today_start, today_end],
            "last_day": [yesterday_start, yesterday_end],
            "weekly": [week_start, week_end],
            "monthly": [month_start, month_end],
            "all": [all_start, all_end],
        }
        time_filter = datetime_map.get(period)
        query = super().get_queryset().filter(owner=self.request.user).filter(
            orders__updated__range=time_filter).annotate(
            new_count=Count('orders', filter=Q(orders__status=Order.OrderStatus.NEW)),
            ready_count=Count('orders', filter=Q(orders__status=Order.OrderStatus.READY_TO_DELIVERY)),
            delivering_count=Count('orders', filter=Q(orders__status=Order.OrderStatus.DELIVERING)),
            delivered_count=Count('orders', filter=Q(orders__status=Order.OrderStatus.DELIVERED)),
            not_count=Count('orders', filter=Q(orders__status=Order.OrderStatus.NOT_CONNECTED)),
            canceled_count=Count('orders', filter=Q(orders__status=Order.OrderStatus.CANCELED)),
            archived_count=Count('orders', filter=Q(orders__status=Order.OrderStatus.ARCHIVED)),
        ).values('name',
                 'product__title',
                 'visit_count',
                 'new_count',
                 'ready_count',
                 'delivering_count',
                 'delivered_count',
                 'not_count',
                 'canceled_count',
                 'archived_count',
                 )
        return query.distinct()

    def get_context_data(self, **kwargs):
        tmp = self.get_queryset().aggregate(
            total_visits=Sum('visit_count'),
            new_total=Sum('new_count'),
            ready_total=Sum('ready_count'),
            delivering_total=Sum('delivering_count'),
            delivered_total=Sum('delivered_count'),
            not_total=Sum('not_count'),
            canceled_total=Sum('canceled_count'),
            archived_total=Sum('archived_count'),
        )
        data = super().get_context_data()
        data.update(tmp)
        return data


class GiveAwayListView(ListView):
    queryset = User.objects.all()
    template_name = 'apps/market/giveaway.html'
    context_object_name = 'sellers'

    def get_queryset(self):
        query = (super().get_queryset().annotate(order_count=Count(
            "threads__orders", filter=Q(threads__orders__status=Order.OrderStatus.DELIVERED))).
                 filter(order_count__gte=1)).values('order_count', 'first_name', 'last_name')
        return query

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['site'] = SiteStatics.objects.first()
        return data


class WithdrawalCreateView(LoginRequiredMixin, CreateView):
    queryset = Withdrawal.objects.all()
    form_class = WithdrawalModelForm
    template_name = 'apps/withdraw/withdraw-form.html'
    success_url = reverse_lazy('withdraw-form')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        user = self.request.user
        user.balance -= form.instance.amount
        user.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        for error in form.errors.values():
            messages.error(self.request, error)
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        data = super().get_form_kwargs()
        data['withdraws'] = Withdrawal.objects.filter(user=self.request.user)
        return data


class OperatorOrderListView(ListView):
    queryset = Order.objects.all()
    template_name = 'apps/operator/operator-page.html'
    context_object_name = 'orders'

    def post(self, request):
        category_id = request.POST.get('category_id')
        district_id = request.POST.get('district_id')
        query = self.get_queryset()
        if category_id:
            query = query.filter(product__category__id=category_id)
        if district_id:
            query = query.filter(district_id=district_id)
        context = {
            "status": Order.OrderStatus.values,
            "categories": Category.objects.all(),
            "orders": query
        }
        return render(request, 'apps/operator/operator-page.html', context)

    def get_queryset(self):
        status = self.request.GET.get('status', 'new')
        category_id = self.request.GET.get('category_id')
        district_id = self.request.GET.get('district_id')
        query = super().get_queryset()
        Order.objects.filter(operator=self.request.user).update(hold=False)
        if category_id:
            query = Order.objects.filter(product__category__id=category_id)
        if district_id:
            query = Order.objects.filter(district_id=district_id)
        if status != 'new':
            query = query.filter(operator=self.request.user, status=status)
        else:
            query = query.filter(status=status)
        return query

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['status'] = Order.OrderStatus.values
        data['regions'] = Region.objects.all()
        data['categories'] = Category.objects.all()
        data['deliver_status'] = [Order.OrderStatus.CANCELED, Order.OrderStatus.DELIVERING, Order.OrderStatus.READY_TO_DELIVERY]
        data['operator_status'] = [Order.OrderStatus.NEW, Order.OrderStatus.CANCELED, Order.OrderStatus.DELIVERED, Order.OrderStatus.DELIVERING,Order.OrderStatus.NOT_CONNECTED, Order.OrderStatus.READY_TO_DELIVERY]
        category_id = self.request.GET.get('category_id')
        district_id = self.request.GET.get('district_id')
        if category_id:
            data['category_id'] = int(category_id)
        if district_id:
            data['district_id'] = int(district_id)
        return data


class OrderUpdateView(LoginRequiredMixin, UpdateView):
    queryset = Order.objects.all()
    template_name = 'apps/operator/order-change.html'
    context_object_name = 'order'
    form_class = OrderUpdateModelForm
    pk_url_kwarg = 'pk'
    success_url = reverse_lazy('operator-page')

    def get(self, request, *args, **kwargs):
        data = super().get(request, *args, **kwargs)
        self.object.hold = True
        return data

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['order'] = self.object
        kwargs['employee'] = self.request.user

        return kwargs

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['regions'] = Region.objects.all()
        return data

    def form_valid(self, form):
        status = form.cleaned_data.get('status')
        obj = self.get_object(self.queryset)
        if obj.thread and status == Order.OrderStatus.DELIVERED.value:
            seller = obj.thread.owner
            seller.balance += (obj.product.seller_price - obj.thread.discount_amount) * obj.quantity
            seller.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        for error in form.errors.values():
            messages.error(self.request, error)
        return super().form_invalid(form)


class DiagramTemplateView(TemplateView):
    template_name = 'apps/diagram/diagram.html'


def diagram_statistic_view(request):
    query = list(Region.objects.annotate(order_count=Count('districts__orders')).values_list('name', 'order_count'))
    res = list(zip(*query))
    data = {
        "regions": res[0],
        "numbers": res[1]
    }
    return JsonResponse(data)
