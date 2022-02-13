from django import template
from ..models import Post
from collections import OrderedDict
from django.db.models import Q
register = template.Library()


@register.inclusion_tag('inc/breaking.html')
def get_breaking_news():
    context = {'posts': Post.objects.filter(is_breaking=True)[:3].select_related('category')}
    return context


@register.inclusion_tag('inc/last_posts.html')
def get_last_news():
    context = {'posts': Post.objects.filter(is_breaking=False)[:6].select_related('category')}
    return context


@register.simple_tag()
def get_categories():
    posts = Post.objects.filter(is_visible=True)[:50].select_related('category')
    container = {}
    for post in posts:
        try:
            container[post.category] += post.views
        except KeyError:
            container[post.category] = post.views
    categories = sorted(container.items(), key=lambda x: x[1], reverse=True)
    if len(categories) > 3:
        hype_categories = OrderedDict(categories[:3])
        all_categories = OrderedDict(categories)
        context = {'hype_categories': hype_categories, 'all_categories': all_categories}
        return context
    context = {'hype_categories': OrderedDict(categories)}
    print(context)
    return context


@register.simple_tag()
def get_related_post(post):
    posts = Post.objects.filter(Q(is_visible=True) and Q(tags__in=post.tags.all())).exclude(pk=post.pk)[:5]
    post_ids = []
    for i in posts.values_list('pk'):
        post_ids.append(i)
    context = {'related_posts': list(posts)}
    while len(context['related_posts']) < 5:
        for post in post.category.posts.filter(is_visible=True).all():
            if post.pk not in post_ids:
                context['related_posts'].append(post)
    return context
