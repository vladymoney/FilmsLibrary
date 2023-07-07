import requests
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from FilmsLibrary.common.forms import UserRegistrationForm

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

def film(request):
    return render(request, 'film.html')