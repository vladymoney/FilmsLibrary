import requests
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views.decorators.csrf import ensure_csrf_cookie

from FilmsLibrary.common.forms import UserRegistrationForm, LoginForm, CommentForm
from FilmsLibrary.common.models import Comment

# Create your views here.

API_KEY = 'e77dc8a60ca530e86fd7b90e4274aee8'
def index(request):
    url = f"https://api.themoviedb.org/3/movie/popular?api_key={API_KEY}"
    response = requests.get(url)
    data = response.json()

    films = []
    if response.status_code == 200 and 'results' in data:
        for film in data['results']:
            film_details = {
                'pk': film['id'],  # Include the film ID (pk)
                'title': film['title'],
                'description': film['overview'],
                'image': f"https://image.tmdb.org/t/p/w500/{film['poster_path']}"
            }
            films.append(film_details)

    return render(request, 'index.html', {'films': films})

def search(request):
    query = request.GET.get('query')
    films = []

    if query:
        url = f"https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&query={query}"
        response = requests.get(url)
        data = response.json()



        if response.status_code == 200 and data['total_results'] > 0:


            for film in data['results']:
                film_details = {
                    'title': film['title'],
                    'description': film['overview'],
                    'image': f"https://image.tmdb.org/t/p/w500/{film['poster_path']}"
                }
                films.append(film_details)

    print(films)  # Debug statement

    return render(request, 'index.html', {'films': films})



def watch_later(request):
    return render(request, 'watch_later.html')


def profile(request):
    return render(request, 'profile.html')


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('index')  # Replace 'success' with the URL name of your success page
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})


def sign_in(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('index')


        form = LoginForm()
        return render(request, 'login.html', {'form': form})

    elif request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                messages.success(request, f'Hi {username.title()}, welcome back!')
                return redirect('index')

        # form is not valid or user is not authenticated
        messages.error(request, f'Invalid username or password')
        return render(request, 'login.html', {'form': form})

@login_required  # Require authentication to submit comments
def film(request, pk):
    url = f"https://api.themoviedb.org/3/movie/{pk}?api_key={API_KEY}"
    response = requests.get(url)
    data = response.json()

    film_details = {
        'title': data['title'],
        'description': data['overview'],
        'image': f"https://image.tmdb.org/t/p/w500/{data['poster_path']}",
        'release_date': data['release_date'],
        'runtime': data['runtime'],
        # Add more fields as needed
    }

    # Handle comment submission
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.film_id = pk
            comment.user_name = request.user.username if request.user.is_authenticated else 'Anonymous'
            comment.save()
            return redirect('film_detail', pk=pk)

    else:
        form = CommentForm()

    # Retrieve comments for the film
    comments = Comment.objects.filter(film_id=pk)

    return render(request, 'film.html', {'film': film_details, 'form': form, 'comments': comments})




def sign_out(request):
    logout(request)
    messages.success(request,f'You have been logged out.')
    return redirect('index')