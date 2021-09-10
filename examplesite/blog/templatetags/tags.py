from django import template
from ..models import Post
from collections import OrderedDict
register = template.Library()


@register.inclusion_tag('blog/inc/breaking.html')
def get_breaking_news():
    context = {'posts': Post.objects.filter(is_breaking=True)[:4]}
    return context


@register.inclusion_tag('blog/inc/last_posts.html')
def get_last_news():
    context = {'posts': Post.objects.filter(is_breaking=False)[:6]}
    return context


@register.simple_tag()
def get_categories():
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
    print(context)
    return context
