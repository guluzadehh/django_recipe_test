from django.urls import path
from .views import *

urlpatterns = [
    path(
        "add-product-to-recipe/",
        view=AddProductToRecipeView.as_view(),
        name="add-product-to-recipe",
    ),
    path("cook-recipe/", view=CookRecipeView.as_view(), name="cook-recipe"),
    path(
        "show-recipes-without-product/",
        view=ShowRecipesWithoutProduct.as_view(),
        name="show-recipes",
    ),
]
