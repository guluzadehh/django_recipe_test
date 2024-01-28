from django.http import HttpRequest, HttpResponse
from django.http.response import HttpResponse
from django.views.generic.base import View
from django.views.generic.list import ListView
from django.shortcuts import get_object_or_404
from django.db.models import F, Q
from .models import RecipeProduct, Recipe, Product


class AddProductToRecipeView(View):
    def get(self, request):
        product_id = request.GET.get("product_id")
        recipe_id = request.GET.get("recipe_id")
        weight = request.GET.get("weight")

        if not product_id or not recipe_id or not weight:
            return HttpResponse(content="Bad request", status=400)

        recipe = get_object_or_404(Recipe, id=recipe_id)
        product = get_object_or_404(Product, id=product_id)

        _, created = RecipeProduct.objects.update_or_create(
            product=product,
            recipe=recipe,
            defaults={"weight": weight},
        )

        return HttpResponse(content="Success", status=201 if created else 200)


class CookRecipeView(View):
    def get(self, request):
        recipe_id = request.GET.get("recipe_id")

        if not recipe_id:
            return HttpResponse(content="Bad request", status=400)

        recipe = get_object_or_404(Recipe, id=recipe_id)

        recipe.products.update(count=F("count") + 1)

        return HttpResponse("Success", status=200)


class ShowRecipesWithoutProduct(ListView):
    model = Recipe
    template_name = "core/recipe-list.html"
    context_object_name = "recipes"

    def get_queryset(self):
        product_id = self.request.GET.get("product_id")
        return Recipe.objects.filter(
            ~Q(recipeproduct__product_id=product_id)
            | Q(
                Q(recipeproduct__product_id=product_id)
                & Q(recipeproduct__weight__lt=10)
            )
        ).distinct()

    def get(self, request: HttpRequest, *args, **kwargs):
        if not request.GET.get("product_id"):
            return HttpResponse("Bad request", status=400)

        return super().get(request, *args, **kwargs)
