from django.urls import path

from FilmsLibrary.common.views import index, watch_later, profile, film, search, register, login

urlpatterns = [
        path('', index, name='index'),
        path('search/', search, name='search'),
        path('watch_later/', watch_later, name='watch later'),
        path('profile/', profile, name='profile'),
        path('film/', film, name='film'),
        path('register/', register, name='register'),
        path('login/', login, name='login'),

]