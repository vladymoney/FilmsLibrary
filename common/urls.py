from django.urls import path

from FilmsLibrary.common.views import index, watch_later, profile, film, search, register, sign_out, sign_in, \
        edit_comment, delete_comment

urlpatterns = [
        path('', index, name='index'),
        path('search/', search, name='search'),
        path('watch_later/', watch_later, name='watch later'),
        path('profile/', profile, name='profile'),
        path('film/<int:pk>/', film, name='film_detail'),
        path('register/', register, name='register'),
        path('login/', sign_in, name='login'),
        path('logout/', sign_out, name='logout'),
        path('comment/edit/<int:comment_id>/', edit_comment, name='edit_comment'),
        path('comment/delete/<int:comment_id>/', delete_comment, name='delete_comment'),

]