from django.contrib import admin
from . import views
from django.urls import path

urlpatterns = [
    path('', views.index, name='index'),
    path('post/<str:slug>/', views.open_post, name='post'),
    path('category/<str:slug>/', views.get_posts_by_category, name='category'),
    path('add_post/', views.add_post, name='add_post')
]