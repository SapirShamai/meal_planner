from django.urls import path
from .views import Register, Login, IngredientViewAndCreate, IngredientByID, RecipeViewAndCreate, RecipeByID

app_name = 'api'

urlpatterns = [
    path('register/', Register.as_view(), name='register'),
    path('login/', Login.as_view(), name='login'),
    path('ingredient/', IngredientViewAndCreate.as_view(), name='ingredient'),
    path('ingredient/<int:ing_id>/', IngredientByID.as_view(), name='ingredient_details'),
    path('recipe/', RecipeViewAndCreate.as_view(), name='recipe'),
    path('recipe/<int:recipe_id>/', RecipeByID.as_view(), name='recipe_details'),


]