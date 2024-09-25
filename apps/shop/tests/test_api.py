import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from model_bakery import baker
from rest_framework.test import APIClient

from apps.shop.models import Cart, CartItem, Category, Product, SubCategory


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def user_factory():
    def factory(*args, **kwargs):
        return baker.make(User, *args, **kwargs)

    return factory


@pytest.fixture
def authenticated_client(client, user_factory):
    """Создаем авторизованного клиента."""
    user = user_factory()
    client.force_authenticate(user=user)
    return client, user


@pytest.fixture
def category_factory():
    def factory(*args, **kwargs):
        return baker.make(Category, *args, **kwargs)

    return factory


@pytest.fixture
def subcategory_factory(category_factory):
    def factory(*args, **kwargs):
        return baker.make(SubCategory, category=category_factory(), *args, **kwargs)

    return factory


@pytest.fixture
def product_factory(subcategory_factory):
    def factory(*args, **kwargs):
        return baker.make(Product, subcategory=subcategory_factory(), *args, **kwargs)

    return factory


@pytest.fixture
def cart_factory(authenticated_client, product_factory):
    def factory(*args, **kwargs):
        client, user = authenticated_client
        cart = baker.make(Cart, user=user)
        product = product_factory()
        baker.make(CartItem, cart=cart, product=product, quantity=2)
        return cart

    return factory


@pytest.mark.django_db
def test_get_categories(client, category_factory):
    """Тест для получения списка категорий."""
    # Создаем фиктивные категории
    category_factory(_quantity=3)

    url = reverse("category-list")
    response = client.get(url)

    assert response.status_code == 200
    assert isinstance(response.data["results"], list)
    assert len(response.data["results"]) == 3


@pytest.mark.django_db
def test_get_cart(authenticated_client, cart_factory):
    """Тест для получения содержимого корзины."""
    client, user = authenticated_client
    cart = cart_factory()

    url = reverse("cart-detail")
    response = client.get(url)

    assert response.status_code == 200
    assert response.data["total_quantity"] == 2
    assert response.data["total_price"] is not None
    assert len(response.data["items"]) == 1


@pytest.mark.django_db
def test_post_add_to_cart(authenticated_client, product_factory):
    """Тест для добавления товара в корзину."""
    client, user = authenticated_client
    product = product_factory()

    url = reverse("cart-detail")
    data = {"product_id": product.id, "quantity": 3}
    response = client.post(url, data, format="json")

    assert response.status_code == 200
    assert (
        response.data["message"]
        == f"Товар {product} успешно добавлен/обновлен в корзине."
    )


@pytest.mark.django_db
def test_post_remove_from_cart(authenticated_client, product_factory):
    """Тест для удаления товара из корзины через POST."""
    client, user = authenticated_client
    product = product_factory()

    url = reverse("cart-detail")
    client.post(url, {"product_id": product.id, "quantity": 2}, format="json")

    response = client.post(
        url, {"product_id": product.id, "quantity": 0}, format="json"
    )

    assert response.status_code == 200
    assert response.data["message"] == f"Товар {product} успешно удален из корзины."


@pytest.mark.django_db
def test_delete_clear_cart(authenticated_client, cart_factory):
    """Тест для полной очистки корзины."""
    client, user = authenticated_client
    cart = cart_factory()

    url = reverse("cart-detail")
    response = client.delete(url)

    assert response.status_code == 200
    assert response.data["message"] == "Корзина успешно очищена."
