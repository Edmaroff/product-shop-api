from django.urls import path

from .views import CartView, CategoryListView, ProductListView

urlpatterns = [
    path("categories/", CategoryListView.as_view(), name="category-list"),
    path("products/", ProductListView.as_view(), name="product-list"),
    path("cart/", CartView.as_view(), name="cart-detail"),
]
