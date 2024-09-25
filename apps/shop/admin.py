from django.contrib import admin
from imagekit.admin import AdminThumbnail

from .models import Category, Product, SubCategory


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", "category"]
    prepopulated_fields = {"slug": ["name"]}


class SubCategoryInline(admin.TabularInline):
    model = SubCategory
    extra = 1
    prepopulated_fields = {"slug": ["name"]}


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    inlines = [SubCategoryInline]
    list_display = ["name", "slug"]
    prepopulated_fields = {"slug": ["name"]}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "price",
        "admin_image",
        "admin_image_small",
        "admin_image_medium",
        "admin_image_large",
    ]
    prepopulated_fields = {"slug": ["name"]}

    admin_image = AdminThumbnail(image_field="image")
    admin_image_small = AdminThumbnail(image_field="image_small")
    admin_image_medium = AdminThumbnail(image_field="image_medium")
    admin_image_large = AdminThumbnail(image_field="image_large")
