from django.shortcuts import render
from django.http import HttpResponse
from .models import Post

# Create your views here.


def index(request):
    return HttpResponse('ssss')


def index(request):
    posts = Post.objects.filter(is_visible=True)
    context = {'posts': posts}
    return HttpResponse(render(request, 'blog/index.html', context))
