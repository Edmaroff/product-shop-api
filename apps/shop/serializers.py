from rest_framework import serializers

from .models import Cart, CartItem, Category, Product, SubCategory


class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ["id", "name", "slug", "image"]


class CategorySerializer(serializers.ModelSerializer):
    subcategories = SubCategorySerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ["id", "name", "slug", "image", "subcategories"]


class ProductSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()

    class Meta:
        fields = ["id", "name", "slug", "price", "subcategory", "images"]
        model = Product
        depth = 2

    def get_images(self, obj):
        """
        Возвращает словарь с URL-адресами изображений продукта разных размеров
        """
        return {
            "original": obj.image.url if obj.image else None,
            "small": obj.image_small.url if obj.image_small else None,
            "medium": obj.image_medium.url if obj.image_medium else None,
            "large": obj.image_large.url if obj.image_large else None,
        }


class CartItemSerializer(serializers.ModelSerializer):
    product = serializers.StringRelatedField()

    class Meta:
        model = CartItem
        fields = ["product", "quantity", "get_total_price"]


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)

    total_quantity = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ["id", "items", "total_quantity", "total_price"]

    def get_total_quantity(self, obj):
        return obj.get_total_quantity()

    def get_total_price(self, obj):
        return obj.get_total_price()
