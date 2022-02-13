from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import Post, Category, Profile
from django.views.generic import ListView, DetailView
from django.db.models import Q, Sum
from collections import OrderedDict
from .forms import PostForm, UserRegisterForm, UserLoginForm, ProfileForm, CommentForm
from datetime import datetime
from django.urls import reverse_lazy, reverse

# Create your views here.


def index(request):
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
            if 'hype_categories' not in context:
                context['hype_categories'] = [{category[0]: category[0].posts.filter(is_visible=True)}]
            else:
                context['hype_categories'].append({category[0]: category[0].posts.filter(is_visible=True)})
    return render(request, 'blog/index.html', context)


def open_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.META.get('HTTP_X_FORWARDED_FOR') or request.META['REMOTE_ADDR']:
        if request.META.get('HTTP_X_FORWARDED_FOR'):
            address = request.META.get('HTTP_X_FORWARDED_FOR')
        else:
            address = request.META['REMOTE_ADDR']
    if (not post.visitors) or (address not in post.visitors):
        if not post.visitors:
            post.visitors = [address]
        else:
            if address not in post.visitors:
                post.visitors.append(address)
        post.update_views()
        post.save()
    liked = False
    if post.likes.filter(id=request.user.id).exists():
        liked = True
    disliked = False
    if post.dislikes.filter(id=request.user.id).exists():
        disliked = True
    form = CommentForm()
    context = {'post': post, 'liked': liked, 'disliked': disliked, 'form': form}
    return render(request, 'blog/post_detail.html', context)


def get_posts_by_category(request, slug):
    context = {'posts': Post.objects.filter(Q(is_visible=True) and Q(category__slug=slug)).select_related('category')}
    return render(request, 'blog/posts.html', context)


def get_posts_by_tag(request, slug):
    context = {'posts': Post.objects.filter(Q(is_visible=True) and Q(tags__slug=slug))}
    return render(request, 'blog/posts.html', context)


def get_breaking(request):
    context = {'posts': Post.objects.filter(is_breaking=True).select_related('category')}
    return render(request, 'blog/posts.html', context)


def get_last_posts(request):
    context = {'posts': Post.objects.filter(is_breaking=False).select_related('category')}
    return render(request, 'blog/posts.html', context)


def add_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save()
            return redirect(post.get_absolute_url())
    else:
        if request.user.is_staff or request.user.is_superuser:
            form = PostForm()
            context = {'form': form}
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
            Profile(user=request.user).save()
            return HttpResponseRedirect(reverse('profile'))
        context = {'form': form}
        return render(request, 'blog/register.html', context)
    else:
        form = UserRegisterForm()
        context = {'form': form}
        return render(request, 'blog/register.html', context)


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        print(form.non_field_errors())
        if form.is_valid():
            login(request, form.get_user())
            return redirect('index')
        context = {'form': form}
        return render(request, 'blog/login.html', context)
    else:
        form = UserLoginForm()
        context = {'form': form}
    return render(request, 'blog/login.html', context)


def user_logout(request):
    logout(request)
    return redirect('login')


def search_posts(request):
    search_post = request.GET.get('search')
    if search_post:
        posts = Post.objects.filter(Q(is_visible=True) and Q(title__icontains=search_post)).select_related('category')
        context = {'posts': posts}
        return render(request, 'blog/search_post.html', context)


def like(request, slug):
    post = get_object_or_404(Post, slug=request.POST.get('post_slug'))
    liked = False
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        liked = False
    else:
        if post.dislikes.filter(id=request.user.id).exists():
            post.dislikes.remove(request.user)
        post.likes.add(request.user)
        liked = True
    return HttpResponseRedirect(reverse('post', args=[slug]))


def dislike(request, slug):
    post = get_object_or_404(Post, slug=request.POST.get('post_slug'))
    disliked = False
    if post.dislikes.filter(id=request.user.id).exists():
        post.dislikes.remove(request.user)
        disliked = False
    else:
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
        post.dislikes.add(request.user)
        disliked = True
    return HttpResponseRedirect(reverse('post', args=[slug]))


def get_user(request):
    if request.POST:
        print(vars(request.POST))
    if not request.user.is_authenticated:
        return redirect('login')
    print(vars(request.user.profile))
    profile = request.user.profile
    form = ProfileForm(instance=request.user.profile)
#    profile = Profile.objects.get(user=request.user)
    print(profile)
    context = {'form': form}
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        context = {'form': form}
        print(form.errors)
        if form.is_valid():
            form.save()
            context = {'form': form}
    print('xx', form)
    return render(request, 'blog/profile.html', context)


def add_comment(request, slug):
    print(slug)
    if request.method == 'POST':
        post = get_object_or_404(Post, slug=request.POST.get('post_slug'))
        form = CommentForm(request.POST)
        form.post = post
        print(request.POST)
        for i in dir(request.POST):
            print(i)
        print(form.is_valid())
        for field in form.fields:
            print(field, form[field].errors)
        print(form['author'].errors)
        print(request.POST.get('author'))
        #print(form)
        #print(form.is_valid())
        #print(form.errors)
        return HttpResponseRedirect(reverse('post', args=[slug]))
    return
