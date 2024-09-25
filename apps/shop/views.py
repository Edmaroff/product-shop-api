from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import generics, permissions, status
from rest_framework.response import Response

from .models import Cart, CartItem, Category, Product
from .pagination import CategoryPagination, ProductPagination
from .serializers import CartSerializer, CategorySerializer, ProductSerializer


@extend_schema(
    tags=["Categories"],
    summary="Получение списка всех категорий",
    responses={200: OpenApiResponse(description="Список категорий с подкатегориями")},
)
class CategoryListView(generics.ListAPIView):
    """Представление для получения списка всех категорий с подкатегориями"""

    queryset = Category.objects.prefetch_related("subcategories").all()
    serializer_class = CategorySerializer
    pagination_class = CategoryPagination


@extend_schema(
    tags=["Products"],
    summary="Получение списка всех продуктов",
    responses={200: OpenApiResponse(description="Список продуктов с изображениями")},
)
class ProductListView(generics.ListAPIView):
    """Представление для получения списка всех продуктов"""

    queryset = Product.objects.select_related("subcategory__category").all()
    serializer_class = ProductSerializer
    pagination_class = ProductPagination


@extend_schema(tags=["Cart"], summary="Работа с корзиной пользователя")
class CartView(generics.GenericAPIView):
    """Представление для работы с корзиной пользователя"""

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CartSerializer

    def get(self, request, *args, **kwargs):
        """Получение содержимого корзины"""
        cart, created = Cart.objects.get_or_create(user=request.user)
        serializer = self.get_serializer(cart)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        """Добавление/обновление товара в корзине."""
        product_id = request.data.get("product_id")
        if not product_id:
            return Response(
                {"error": "Не указан product_id."}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response(
                {"error": "Продукт с указанным product_id не существует."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        quantity = request.data.get("quantity", 1)
        try:
            quantity = int(quantity)
            if quantity < 0:
                return Response(
                    {"error": "Количество товара не может быть отрицательным."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except ValueError:
            return Response(
                {"error": "Количество товара должно быть целым числом."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
            return Response(
                {"message": f"Товар {product} успешно добавлен/обновлен в корзине."},
                status=status.HTTP_200_OK,
            )
        else:
            cart_item.delete()
            return Response(
                {"message": f"Товар {product} успешно удален из корзины."},
                status=status.HTTP_200_OK,
            )

    def delete(self, request, *args, **kwargs):
        """Полная очистка корзины"""
        try:
            cart = Cart.objects.get(user=request.user)
        except Cart.DoesNotExist:
            return Response(
                {"error": "Корзина пользователя не найдена."},
                status=status.HTTP_404_NOT_FOUND,
            )

        cart.items.all().delete()
        return Response(
            {"message": "Корзина успешно очищена."}, status=status.HTTP_200_OK
        )
