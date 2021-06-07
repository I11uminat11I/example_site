from django.contrib import admin

# Register your models here.
from django.utils.safestring import mark_safe

from .models import Post, Category, Tag
image_type = ['jpg', 'png', 'gif']
video_type = ['mp4', 'webm']
audio_type = ['mp3']


class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    model = Post
    list_display = ['id', 'title', 'category', 'slug', 'is_visible', 'get_media', 'created_at']
    list_display_links = ['id', 'title']
    readonly_fields = ('views', 'created_at', 'get_media')
    search_fields = ['title']
    list_filter = ['category', 'tags', 'created_at']
    fields = ('title', 'category', 'content', 'tags', 'slug', 'views', 'is_visible', 'file', 'get_media', 'created_at',)
    list_per_page = 5
    save_on_top = True

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
