import json
import datetime

from django.http import JsonResponse
from django.views.generic import DetailView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from store.models import Order, Category, Product, OrderItem, ShippingAddress
from store.filters import ProductFilter


class HomeView(LoginRequiredMixin, TemplateView):
    """Home view"""

    template_name = "store/home.html"
    login_url = "login/"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        customer = self.request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        context["cartItems"] = order.get_cart_items
        context["category"] = Category.objects.all()
        return context


class StoreView(LoginRequiredMixin, DetailView):
    """Store detail view"""

    template_name = "store/store.html"
    login_url = "login/"
    model = Product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order, created = Order.objects.get_or_create(
            customer=self.request.user, complete=False
        )
        context["cartItems"] = order.get_cart_items

        myFilter = ProductFilter(
            self.request.GET,
            queryset=Product.objects.filter(
                category=Category.objects.get(pk=self.kwargs["pk"])
            ),
        )
        context["products"] = myFilter.qs
        context["myFilter"] = myFilter
        return context


class DescriptionView(LoginRequiredMixin, DetailView):
    template_name = "store/description.html"
    login_url = "login/"
    model = Product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["products"] = Product.objects.filter(pk=self.kwargs["pk"])
        return context


class CartView(LoginRequiredMixin, TemplateView):
    template_name = "store/cart.html"
    login_url = "login/"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order, created = Order.objects.get_or_create(
            customer=self.request.user, complete=False
        )
        context["order"] = order
        context["items"] = order.orderitem_set.all()
        context["cartItems"] = order.get_cart_items
        return context


class CheckoutView(LoginRequiredMixin, TemplateView):
    template_name = "store/checkout.html"
    login_url = "login/"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order, created = Order.objects.get_or_create(
            customer=self.request.user, complete=False
        )
        context["order"] = order
        context["items"] = order.orderitem_set.all()
        context["cartItems"] = order.get_cart_items
        return context


def update_item(request):
    data = json.loads(request.body)
    productId = data["productId"]
    action = data["action"]

    print("Action : ", action)
    print("ProductId : ", productId)

    customer = request.user
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == "add":
        orderItem.quantity = orderItem.quantity + 1
    elif action == "remove":
        orderItem.quantity = orderItem.quantity - 1

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse("Item was added", safe=False)


def process_order(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        total = float(data["form"]["total"])
        order.transaction_id = transaction_id

        if total == order.get_cart_total:
            order.complete = True
        order.save()

        if order.shipping == True:
            ShippingAddress.objects.create(
                customer=customer,
                order=order,
                address=data["shipping"]["address"],
                city=data["shipping"]["city"],
                state=data["shipping"]["state"],
                zipcode=data["shipping"]["zipcode"],
            )

    else:
        print("User is not logged in")
    return JsonResponse("Payment complete", safe=False)
