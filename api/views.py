from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.views import APIView
from .serializers import RegisterSerializer, LoginSerializer, IngredientSerializer, RecipeSerializer, \
    RecipeIngredientSerializer
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from recipes.models import Ingredient, Recipe, RecipeIngredient
from django.http import Http404


class Register(APIView):
    """ register new user and create token"""

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            # create user with hashed password:
            user = User.objects.create_user(**serializer.data)
            # create token:
            Token.objects.create(user=user)
            return Response(serializer.data)
        return Response(serializer.errors)


class Login(APIView):
    """ login user return username and token or empty dict if no matching user"""

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(**serializer.data)
            if user is not None:
                token = Token.objects.get(user=user)
                data = {'token': str(token), 'username': user.username}
                return Response(data)
        return Response(serializer.errors)


class IngredientViewAndCreate(APIView):
    """ ingredient api view for get and post request """

    def get(self, request):
        """ list all ingredient """
        ingredients = Ingredient.objects.all()
        serializer = IngredientSerializer(ingredients, many=True)
        return Response(serializer.data)

    def post(self, request):
        """ create new ingredient """
        ingredient = request.data
        serializer = IngredientSerializer(data=ingredient)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)


class IngredientByID(APIView):
    """ ingredient api view for get put and delete by id """

    def get_object(self, ing_id):
        """ get the ingredient if exist"""
        try:
            return Ingredient.objects.get(id=ing_id)
        except Ingredient.DoesNotExist:
            raise Http404

    def get(self, request, ing_id: int):
        """ view ingredient details """

        ingredient = self.get_object(ing_id)
        serializer = IngredientSerializer(ingredient)
        return Response(serializer.data)

    def put(self, request, ing_id: int):
        """ change ingredient details """
        ingredient = self.get_object(ing_id)
        serializer = IngredientSerializer(ingredient, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    def delete(self, request, ing_id: int):
        """ delete ingredient by id """
        ingredient = self.get_object(ing_id)
        ingredient.delete()
        return Response({"message": "Ingredient was successfully deleted"}, status=204)

    def handle_exception(self, exc):
        """ add custom error handling """
        if isinstance(exc, Http404):  # check if exception is http404
            return Response({"error": "Ingredient does not exist"}, status=404)
        return super().handle_exception(exc)


class RecipeViewAndCreate(APIView):
    """ recipe api view for get and post request """

    def get(self, request):
        """ list all ingredient """
        recipes = Recipe.objects.all()
        serializer = RecipeSerializer(recipes, many=True)
        return Response(serializer.data)

    def post(self, request):
        """ create new ingredient """
        recipe = request.data
        serializer = RecipeSerializer(data=recipe)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)


class RecipeByID(APIView):
    """ recipe api view for get put and delete by id """

    def get_object(self, recipe_id):
        """ get recipe object """
        try:
            return Recipe.objects.get(id=recipe_id)
        except Recipe.DoesNotExist:
            raise Http404

    def get(self, request, recipe_id: int):
        """ view recipe details """
        recipe = self.get_object(recipe_id)
        serializer = RecipeSerializer(recipe)
        return Response(serializer.data)

    def put(self, request, recipe_id: int):
        """ change recipe details """
        recipe = self.get_object(recipe_id)
        serializer = RecipeSerializer(recipe, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    def delete(self, request, recipe_id: int):
        """ delete recipe by id """
        recipe = self.get_object(recipe_id)
        recipe.delete()
        return Response({"message": "Recipe was successfully deleted"}, status=204)

    def handle_exception(self, exc):
        """ add custom error handling """
        if isinstance(exc, Http404):
            return Response({"error": "Recipe does not exist"}, status=404)
        return super().handle_exception(exc)
