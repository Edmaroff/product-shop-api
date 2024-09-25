<img src="https://img.shields.io/badge/python-3.12-blue" alt="Python version"/> <img src="https://img.shields.io/badge/django-5.1-blue" alt="Django Version"/> <img src="https://img.shields.io/badge/Django%20REST%20framework-3.15-blue" alt="Django REST Framework Version"/>
<h1>Product Shop API</h1>

<h2>Описание</h2>

<p>Product Shop API — это API для интернет-магазина, реализованное с помощью Django и 
Django REST Framework. API предоставляет функциональность для управления категориями, 
подкатегориями и продуктами, а также для работы с корзиной пользователя и регистрацией.<p>



<h2>Функциональность</h2>

<ul>
  <li><strong>Категории и подкатегории</strong>:
    <ul>
      <li>Создание, редактирование, удаление категорий и подкатегорий.</li>
      <li>Категории и подкатегории содержат наименование, slug, изображение.</li>
      <li>Подкатегории связаны с родительской категорией.</li>
    </ul>
  </li>
  <li><strong>Продукты</strong>:
    <ul>
      <li>Продукты привязаны к подкатегориям.</li>
      <li>Продукты имеют наименование, slug, изображение в 3-х размерах и цену.</li>
    </ul>
  </li>
  <li><strong>Корзина</strong>:
    <ul>
      <li>Добавление, изменение количества и удаление продуктов в корзине.</li>
      <li>Подсчет количества товаров и общей суммы товаров в корзине.</li>
      <li>Полная очистка корзины.</li>
    </ul>
  </li>
  <li><strong>Регистрация пользователей</strong>:
    <ul>
      <li>Регистрация нового пользователя с JWT-аутентификацией.</li>
    </ul>
  </li>
  <li><strong>API документация</strong>:
    <ul>
      <li>Документация через Swagger UI.</li>
    </ul>
  </li>
</ul>



<details >
  <summary><h2>Технологии</h2></summary>
    <ul>
      <li>Django</li>
      <li>Django REST framework</li>
      <li>PostgreSQL</li>
      <li>drf-spectacular</li>
      <li>Imagekit</li>
      <li>Pytest</li>
    </ul>
</details>


<h2>Запуск проекта (Windows)</h2>


<ol>
  <li>Клонируйте репозиторий:
    <pre><code>git clone https://github.com/Edmaroff/product-shop-api</code></pre>
  </li>
  <li>Перейдите в директорию проекта:
    <pre><code>cd product-shop-api</code></pre>
  </li>

  <li>Установите и активируйте виртуальное окружение для проекта <code>venv</code>:
      <pre><code>python -m venv venv
venv\Scripts\activate</code></pre>
  </li>
  <li>Установите зависимости из <code>requirements.txt</code>:
    <pre><code>pip install -r requirements.txt</code></pre>
  </li>
  <li>Примените миграции:
    <pre><code>python manage.py migrate</code></pre>
  </li>
  <li>Загрузите фикстуру в БД:
    <pre><code>python manage.py loaddata .\apps\shop\fixtures\shop_data.json</code></pre>
  </li>

  <li>Запустите сервер:
    <pre><code>python manage.py runserver</code></pre>
  </li>
</ol>
<hr>


<h2>Запуск тестов</h2>
<ol>
  <li>Запустите тесты с помощью Pytest:
    <pre><code>pytest</code></pre>
  </li>
</ol>
