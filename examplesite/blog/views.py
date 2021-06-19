from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Post, Category
from django.views.generic import ListView, DetailView
from django.db.models import Q

# Create your views here.


def index(request):
    search_post = request.GET.get('search')
    if search_post:
        posts = Post.objects.filter(Q(is_visible=True) and Q(title__icontains=search_post))
        context = {'posts': posts}
        return render(request, 'blog/index.html', context)
    posts = Post.objects.filter(is_visible=True)
    context = {'posts': posts}
    return render(request, 'blog/index.html', context)


def open_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    return render(request, 'blog/post_detail.html', {'post': post})


def get_posts_by_category(request, slug):
    posts = Post.objects.filter(category__slug=slug)
    return render(request, 'blog/posts.html', {'posts': posts})


