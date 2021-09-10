from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Post, Category
from django.views.generic import ListView, DetailView
from django.db.models import Q, Sum
from collections import OrderedDict
from .forms import PostForm, UserRegisterForm, UserLoginForm
from datetime import datetime

# Create your views here.


def index(request):
    search_post = request.GET.get('search')
    if search_post:
        posts = Post.objects.filter(Q(is_visible=True) and Q(title__icontains=search_post))
        context = sort_categories()
        context['posts'] = posts
        return render(request, 'blog/index.html', context)
    get_categories = Category.objects.all()
    categories_list = {}
    for category in get_categories:
        posts_by_category = category.posts.filter(is_visible=True).aggregate(category_views=Sum('views'))
        views = posts_by_category['category_views']
        if views:
            categories_list[category] = views
    if categories_list:
        context = {}
        hype_categories = sorted(categories_list.items(), key=lambda x: x[1], reverse=True)[:3]
        for category in hype_categories:
            print(category[0].posts.filter(is_visible=True))
            if not 'hype_categories' in context:
                context['hype_categories'] = [{category[0]: category[0].posts.filter(is_visible=True)}]
            else:
                context['hype_categories'].append({category[0]: category[0].posts.filter(is_visible=True)})
    print('start')
    for category in context['hype_categories']:
        print('category:', category)
        for post in category.values():
            print('posts:', post)
        print('/' * 10)

    print(context)
    return render(request, 'blog/index.html', context)


def open_post(request, slug):
    context = sort_categories()
    post = get_object_or_404(Post, slug=slug)
    print(post)
    post.views += 1
    post.save()
    context['post'] = post
    return render(request, 'blog/post_detail.html', context)


def get_posts_by_category(request, slug):
    context = sort_categories()
    context['posts'] = Post.objects.filter(Q(is_visible=True) and Q(category__slug=slug))
    return render(request, 'blog/posts.html', context)


def get_breaking(request):
    context = {'posts': Post.objects.filter(is_breaking=True)}
    return render(request, 'blog/posts.html', context)


def get_last_posts(request):
    context = {'posts': Post.objects.filter(is_breaking=False)}
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
            context = sort_categories()
            context['form'] = form
            return render(request, 'blog/add_post.html', context)
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
        context = sort_categories()
        context['form'] = form
    return render(request, 'blog/register.html', context)


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('index')
    else:
        form = UserLoginForm()
        context = sort_categories()
        context['form'] = form
    return render(request, 'blog/login.html', context)


def user_logout(request):
    logout(request)
    return redirect('login')

def test():
    get_categories = Category.objects.all()
    categories_list = {}
    for category in get_categories:
        posts_by_category = category.posts.all().aggregate(category_views=Sum('views'))
        views = posts_by_category['category_views']
        if views:
            categories_list[category] = views
    return categories_list