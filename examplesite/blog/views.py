from django.shortcuts import render
from django.http import HttpResponse
from .models import Post

# Create your views here.


def index(request):
    return HttpResponse('ssss')


def show_posts(request):
    posts = Post.objects.filter(is_visible=True)
    return HttpResponse(render(request, 'blog/show_posts.html', posts))
