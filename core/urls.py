from django.contrib import admin
from django.urls import path
from core.views import index, login_view, post_detail, register, archive, create_post, my_posts, logout_view, like_post, edit_post, delete_post

urlpatterns = [
    path('', index, name='index'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('post/<int:id>/', post_detail, name='post_detail'),
    path('post/<int:id>/like/', like_post, name='like_post'),
    path('post/<int:id>/edit/', edit_post, name='edit_post'),
    path('post/<int:id>/delete/', delete_post, name='delete_post'),
    path('register/', register, name='register'),
    path('create_post/', create_post, name='create_post'),
    path('archive/', archive, name='archive'),
    path('my_posts/', my_posts, name='my_posts'),
]
