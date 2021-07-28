from ckeditor_uploader.widgets import CKEditorUploadingWidget
from ckeditor.fields import RichTextField
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

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


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(label='Enter your name', widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.CharField(label='Enter your email', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='Enter your password', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Confirm your password', widget=forms.TextInput(attrs={'class': 'form-control'}))


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Enter your name', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Enter your password', widget=forms.TextInput(attrs={'class': 'form-control'}))
