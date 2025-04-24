from django.urls import path
from django_app import get_posts, get_post, create_post

urlpatterns = [
    path('posts', get_posts, name='get_posts'),
    path('posts/<str:id>', get_post, name='get_post'),
    path('posts/create', create_post, name='create_post'),
]