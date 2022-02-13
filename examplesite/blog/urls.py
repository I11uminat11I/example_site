from django.contrib import admin
from . import views
from django.urls import path

urlpatterns = [
    path('', views.index, name='index'),
    path('post/<str:slug>/', views.open_post, name='post'),
    path('category/<str:slug>/', views.get_posts_by_category, name='category'),
    path('tag/<str:slug>/', views.get_posts_by_tag, name='tag'),
    path('add_post/', views.add_post, name='add_post'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('breaking/', views.get_breaking, name='breaking_news'),
    path('last_posts/', views.get_last_posts, name='last_news'),
    path('search_post/', views.search_posts, name='search_post'),
    path('like/<str:slug>', views.like, name='like'),
    path('dislike/<str:slug>', views.dislike, name='dislike'),
    path('profile/', views.get_user, name='profile'),
    path('add_comment/<str:slug>', views.add_comment, name='add_comment')
]