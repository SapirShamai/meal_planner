from rest_framework import serializers
from recipes.models import Ingredient, Recipe, RecipeIngredient


class RegisterSerializer(serializers.Serializer):
    """ register serializer """
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255)
    email = serializers.EmailField()
    first_name = serializers.CharField(max_length=255, required=False)
    last_name = serializers.CharField(max_length=255, required=False)


class LoginSerializer(serializers.Serializer):
    """  login serializer"""
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255)


class IngredientSerializer(serializers.ModelSerializer):
    """ Ingredient serializer """
    class Meta:
        model = Ingredient
        fields = ['id', 'name']


class RecipeIngredientSerializer(serializers.ModelSerializer):
    """ RecipeIngredient serializer """
    ingredient = IngredientSerializer(read_only=True)
    ingredient_id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all(), write_only=True)

    class Meta:
        model = RecipeIngredient
        fields = ['ingredient', 'ingredient_id', 'quantity']


class RecipeSerializer(serializers.ModelSerializer):
    """ Recipe serializer """
    ingredients = RecipeIngredientSerializer(source='recipeingredient_set', many=True)
    user = serializers.ReadOnlyField(source='user.id')

    class Meta:
        model = Recipe
        fields = ['id', 'title', 'description', 'cooking_instructions', 'image', 'ingredients', 'user', 'is_public']

    def create(self, validated_data):
        ingredients_data = validated_data.pop('recipeingredient_set')  # remove ingredients from data
        recipe = Recipe.objects.create(**validated_data)
        for ingredient_data in ingredients_data:
            RecipeIngredient.objects.create(recipe=recipe, **ingredient_data)
        return recipe

    def update(self, instance, validated_data):
        ingredients_data = validated_data.pop('recipeingredient_set')  # remove ingredients from data
        instance = super().update(instance, validated_data)    # update the rest of the data
        for ingredient_data in ingredients_data:
            ingredient_id = ingredient_data.get('ingredient').id
            RecipeIngredient.objects.get_or_create(
                recipe=instance, ingredient_id=ingredient_id, quantity=ingredient_data.get('quantity'))
        return instance
