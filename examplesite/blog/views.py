from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Post, Category
from django.views.generic import ListView, DetailView
from django.db.models import Q
from collections import OrderedDict
from .forms import PostForm, UserRegisterForm, UserLoginForm

# Create your views here.


def index(request):
    search_post = request.GET.get('search')
    if search_post:
        posts = Post.objects.filter(Q(is_visible=True) and Q(title__icontains=search_post))
        context = {'posts': posts}
        return render(request, 'blog/index.html', context)
    posts = Post.objects.filter(is_visible=True)
#    context = {'posts': posts}
    context = sort_categories()
    context['posts'] = posts
    return render(request, 'blog/index.html', context)


def open_post(request, slug):
    context = sort_categories()
    context['post'] = get_object_or_404(Post, slug=slug)
    return render(request, 'blog/post_detail.html', context)


def get_posts_by_category(request, slug):
    context = sort_categories()
    context['posts'] = Post.objects.filter(Q(is_visible=True) and Q(category__slug=slug))
    return render(request, 'blog/posts.html', context)


def sort_categories():
    posts = Post.objects.filter(is_visible=True)[:50]
    container = {}
    for post in posts:
        try:
            container[post.category] += post.views
        except KeyError:
            container[post.category] = post.views
    categories = sorted(container.items(), key=lambda x: x[1], reverse=True)
    if len(categories) > 3:
        hype_categories = OrderedDict(categories[:3])
        other_categories = OrderedDict(categories[3:])
        context = {'hype_categories': hype_categories, 'other_categories': other_categories}
        return context
    context = {'hype_categories': OrderedDict(categories)}
    return context


def add_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save()
            return redirect(post.get_absolute_url())
    else:
        if request.user.is_staff or request.user.is_superuser:
            form = PostForm()
            return render(request, 'blog/add_post.html', {'form': form})
        return redirect('login')


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password1']
            form.save()
            user = authenticate(request, username=username, password=password)
            login(request, user)
            return redirect('index')
    else:
        form = UserRegisterForm()
    return render(request, 'blog/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('index')
    else:
        form = UserLoginForm()
    return render(request, 'blog/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('login')
