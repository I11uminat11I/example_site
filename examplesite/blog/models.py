from django.db import models

# Create your models here.
from django.db import models
from django.urls import reverse, reverse_lazy
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from mptt.models import MPTTModel, TreeForeignKey


class Category(models.Model):
    title = models.CharField(max_length=150)
    slug = models.SlugField(max_length=150, unique=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse_lazy('category', kwargs={'slug': self.slug})

    class Meta:
        ordering = ['title']
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Tag(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('tag', kwargs={'slug': self.slug})

    class Meta:
        ordering = ['title']


class Post(models.Model):
    title = models.CharField(max_length=150)
    slug = models.SlugField(max_length=150, unique=True)
    content = models.TextField(blank=True)
    short_description = models.CharField(max_length=300, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    file = models.FileField(upload_to='uploads/%Y/%m/%d/', blank=True)
    image = models.ImageField(upload_to='covers/%Y/%m/%d/', blank=True)
    views = models.IntegerField(default=0)
    tags = models.ManyToManyField(Tag, related_name='posts', blank=True)
    is_visible = models.BooleanField(default=True)
    is_breaking = models.BooleanField(default=False)
    category = models.ForeignKey(Category, models.PROTECT, related_name='posts')
    visitors = models.JSONField(null=True, default=None)
    likes = models.ManyToManyField(User, blank=True, related_name='likes')
    dislikes = models.ManyToManyField(User, blank=True, related_name='dislikes')

    def update_views(self):
        self.views = len(self.visitors)
        return self.views

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        return super(Post, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post', kwargs={'slug': self.slug})

    class Meta:
        ordering = ['-created_at']


class Comment(MPTTModel):
    parent = TreeForeignKey('self', on_delete=models.CASCADE, related_name='children', blank=True, null=True, default='')
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    content = models.TextField()
    added = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, related_name='comment_author', on_delete=models.CASCADE)

    def __str__(self):
        return '%s - %s' % (self.post.title, self.author)

    class MPTTMeta:
        order_insertion_by = ['added']


class Profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=30, null=True)
    avatar = models.ImageField(upload_to='avatars/%Y/%m/%d/', blank=True, null=True)
    email = models.CharField(max_length=200, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    phoneNumberRegex = RegexValidator(regex=r"^\+?1?\d{8,15}$")
    phoneNumber = models.CharField(validators=[phoneNumberRegex], max_length=16, unique=True, null=True)

    def __str__(self):
        return str(self.user)
