from django.db import models


class Ingredient(models.Model):
    """ ingredient model """
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """ recipe model """
    title = models.CharField(max_length=255)
    description = models.TextField()
    ingredients = models.ManyToManyField(Ingredient, through='RecipeIngredient')
    cooking_instructions = models.TextField()
    image = models.ImageField(upload_to='recipes/', null=True, blank=True)

    def __str__(self):
        return self.title


class RecipeIngredient(models.Model):
    """ This model represents the relationship between Recipe and Ingredient """
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.CharField(max_length=100)

    def __str__(self):
        return str(self.recipe)


