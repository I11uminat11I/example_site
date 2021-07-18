from ckeditor_uploader.widgets import CKEditorUploadingWidget
from ckeditor.fields import RichTextField
from django import forms
from .models import Post


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['title', 'content', 'is_visible', 'category', 'tags', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'tags': forms.SelectMultiple(attrs={'class': 'form-select'}),
            'content': CKEditorUploadingWidget(),
            'image': forms.FileInput(attrs={'class': "form-control"}),
            'is_visible': forms.CheckboxInput(attrs={'class': "form-check-input"})
        }
