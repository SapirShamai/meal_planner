from django.urls import path
from .views import recipe_list, recipe_by_id

app_name = 'recipes'

urlpatterns = [
    path('recipe_list/', recipe_list, name='recipe_list'),
    path('recipe_details/<int:recipe_id>', recipe_by_id, name='recipe_details'),



]
