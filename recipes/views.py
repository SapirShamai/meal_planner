from django.shortcuts import render
import requests


def recipe_list(request):
    """ list all recipes """
    api_url = 'http://127.0.0.1:8000/api/recipe/'
    response = requests.get(api_url)
    recipes = response.json()
    return render(request, 'recipe_list.html', {'recipes': recipes})


def recipe_by_id(request, recipe_id):
    """ view recipe by id """
    api_url = f'http://127.0.0.1:8000/api/recipe/{recipe_id}/'
    response = requests.get(api_url)
    recipe = response.json()
    return render(request, 'recipe_details.html', {'recipe': recipe})
