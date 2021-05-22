from django.db import models

# Create your models here.
from django.db import models


class Category(models.Model):
    title = models.CharField(max_length=150)
    slug = models.SlugField(max_length=150, unique=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']


class Tag(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']


class Post(models.Model):
    title = models.CharField(max_length=150)
    slug = models.SlugField(max_length=150, unique=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    file = models.FileField(upload_to='uploads/%Y/%m/%d/')
    views = models.IntegerField(default=0)
    tags = models.ManyToManyField(Tag, related_name='posts')
    is_visible = models.BooleanField(default=True)
    category = models.ForeignKey(Category, models.PROTECT, related_name='posts')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']

