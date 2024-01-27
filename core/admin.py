from django.contrib import admin
from .models import Recipe, Product, RecipeProduct


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "count")
    list_editable = ("name",)


class ProductsInline(admin.TabularInline):
    model = Recipe.products.through


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    list_editable = ("name",)
    inlines = (ProductsInline,)
