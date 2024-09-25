from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify
from imagekit.models import ImageSpecField
from imagekit.processors import Adjust, ResizeToFill, ResizeToFit


class Category(models.Model):
    """Модель для представления категорий товаров"""

    name = models.CharField(verbose_name="Название", max_length=90, unique=True)
    slug = models.SlugField(
        verbose_name="Слаг", max_length=120, unique=True, blank=True
    )
    image = models.ImageField(
        verbose_name="Фото", upload_to="images/categories/", blank=True, null=True
    )

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Список категорий"
        ordering = ("-name",)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    """Модель для представления подкатегорий товаров"""

    name = models.CharField(verbose_name="Название", max_length=90, unique=True)
    slug = models.SlugField(
        verbose_name="Слаг", max_length=120, unique=True, blank=True
    )
    image = models.ImageField(
        verbose_name="Фото", upload_to="images/subcategories/", blank=True, null=True
    )
    category = models.ForeignKey(
        Category,
        verbose_name="Категория",
        related_name="subcategories",
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = "Подкатегория"
        verbose_name_plural = "Список подкатегорий"
        ordering = ("-name",)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Product(models.Model):
    """Модель для представления продуктов."""

    name = models.CharField(verbose_name="Название", max_length=150, unique=True)
    slug = models.SlugField(
        verbose_name="Слаг", max_length=200, blank=True, unique=True
    )
    subcategory = models.ForeignKey(
        SubCategory,
        verbose_name="Подкатегория",
        related_name="products",
        on_delete=models.CASCADE,
    )
    price = models.DecimalField(verbose_name="Цена", max_digits=10, decimal_places=2)
    image = models.ImageField(verbose_name="Фото", upload_to="images/products/")

    # Генерируемые изображения с разными размерами
    image_small = ImageSpecField(
        source="image",
        processors=[ResizeToFill(50, 50), Adjust(contrast=1.2, sharpness=1.1)],
        format="JPEG",
        options={"quality": 80},
    )
    image_medium = ImageSpecField(
        source="image",
        processors=[ResizeToFit(300, 200), Adjust(contrast=1.2, sharpness=1.1)],
        format="JPEG",
        options={"quality": 80},
    )
    image_large = ImageSpecField(
        source="image",
        processors=[
            ResizeToFit(640, 480),
            Adjust(contrast=1.2, sharpness=1.1),
        ],
        format="JPEG",
        options={"quality": 80},
    )

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Список продуктов"
        ordering = ("-name",)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Cart(models.Model):
    """Модель для представления корзины пользователя"""

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="cart")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Корзина пользователя {self.user.username}"

    def get_total_quantity(self):
        """Возвращает общее количество товаров в корзине"""
        return sum(item.quantity for item in self.items.all())

    def get_total_price(self):
        """Возвращает общую стоимость товаров в корзине"""
        return sum(item.get_total_price() for item in self.items.all())


class CartItem(models.Model):
    """Модель для представления элемента корзины"""

    cart = models.ForeignKey(Cart, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.product.name}"

    def get_total_price(self):
        """Возвращает общую стоимость данного товара в корзине"""
        return self.product.price * self.quantity
