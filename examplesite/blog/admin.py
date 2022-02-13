from ckeditor.widgets import CKEditorWidget
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.contrib import admin
from mptt.admin import MPTTModelAdmin

# Register your models here.
from django.utils.safestring import mark_safe
from django import forms

from .models import Post, Category, Tag, Comment, Profile

image_type = ['jpg', 'png', 'gif']
video_type = ['mp4', 'webm']
audio_type = ['mp3']


class PostAdminForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    content = forms.CharField(widget=CKEditorUploadingWidget())
    short_description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}))
    category = forms.Select(attrs={'class': 'form-select'}),
    tags = forms.MultipleChoiceField(widget=forms.SelectMultiple(attrs={'class': 'form-select'})),
    image = forms.FileInput(attrs={'class': 'form-control', 'type': 'file', 'id': 'formFile'}),
    is_visible = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': "form-check-input"}))

    class Meta:
        model = Post
        fields = '__all__'


class PostAdmin(admin.ModelAdmin):
    form = PostAdminForm
    prepopulated_fields = {"slug": ("title",)}
    model = Post
    list_display = ['id', 'title', 'category', 'slug', 'is_visible', 'get_image', 'created_at', 'is_breaking']
    list_display_links = ['id', 'title']
    readonly_fields = ('views', 'created_at', 'get_image')
    search_fields = ['title']
    list_filter = ['category', 'tags', 'created_at', 'is_breaking']
    fields = ('title', 'category', 'short_description', 'content', 'tags', 'slug', 'likes', 'dislikes', 'views', 'is_visible', 'image',
              'get_image', 'created_at', 'is_breaking')
    list_per_page = 5
    save_on_top = True

    def get_image(self, obj):
        if obj.image:
            return mark_safe(f'<image src="{obj.image.url}" width=80px">')

    get_image.short_description = 'image'

    def get_media(self, obj):
        print(obj.file)
        name = str(obj.file)
        if name.split('.')[-1] in image_type:
            return mark_safe(f'<image src="{obj.file.url}" height=60px">')
        if name.split('.')[-1] in video_type:
            return mark_safe(f'<video src="{obj.file.url}" height=60px">')
        if name.split('.')[-1] in audio_type:
            return mark_safe(f'<audio src="{obj.file.url}" height=600px">')
        return 'No media'
    get_media.short_description = 'media'


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}


class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}


admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Comment, MPTTModelAdmin)
admin.site.register(Profile)

admin.site.site_header = 'The Green Elephant News'
admin.site.site_title = 'The Green Elephant News'
