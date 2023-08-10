import requests
from django.shortcuts import render, redirect
from users.forms.register_form import RegisterForm
from users.forms.login_form import LoginForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


def home_view(request):
    """ render the home page """
    return render(request, 'home.html')


def register_view(request):
    """ register new user """
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            api_url = 'http://127.0.0.1:8000/api/register/'
            response = requests.post(api_url, data=form.cleaned_data)
            if response.status_code == 200:
                username = form.cleaned_data.get('username')
                raw_password = form.cleaned_data.get('password')
                user = authenticate(username=username, password=raw_password)
                login(request, user)
                return redirect('recipes:recipe_list')
            else:
                messages.error(request, 'Registration error. Please try again.')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})


def login_view(request):
    """ login user """
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('recipes:recipe_list')
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    """ logout user and redirect to home page """
    logout(request)
    return redirect('home')
