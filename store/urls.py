from django.urls import path
from store.views import (
    HomeView,
    StoreView,
    DescriptionView,
    CartView,
    update_item,
    CheckoutView,
    process_order,
)


urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("store/<int:pk>/", StoreView.as_view(), name="store"),
    path("description/<int:pk>/", DescriptionView.as_view(), name="description"),
    path("cart", CartView.as_view(), name="cart"),
    path("update_item/", update_item, name="update_item"),
    path("checkout/", CheckoutView.as_view(), name="checkout"),
    path('process_order/', process_order, name="process_order"),
]
