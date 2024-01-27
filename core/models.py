from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=255)
    count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    name = models.CharField(max_length=255)
    products = models.ManyToManyField(
        Product, through="RecipeProduct", related_name="products"
    )

    def __str__(self):
        return self.name


class RecipeProduct(models.Model):
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=("product_id", "recipe_id"), name="unique_recipe_product"
            )
        ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    weight = models.PositiveIntegerField()
