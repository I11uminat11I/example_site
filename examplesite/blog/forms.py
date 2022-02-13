from ckeditor_uploader.widgets import CKEditorUploadingWidget
from ckeditor.fields import RichTextField
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Post, Profile, Comment
from mptt.forms import TreeNodeChoiceField


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['title', 'content', 'short_description', 'is_visible', 'category', 'tags', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'short_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'tags': forms.SelectMultiple(attrs={'class': 'form-select'}),
            'content': CKEditorUploadingWidget(),
            'image': forms.FileInput(attrs={'class': "form-control"}),
            'is_visible': forms.CheckboxInput(attrs={'class': "form-check-input"}),
        }


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(label='Enter your name', widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.CharField(label='Enter your email', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='Enter your password', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Confirm your password', widget=forms.TextInput(attrs={'class': 'form-control'}))


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Enter your name', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Enter your password', widget=forms.TextInput(attrs={'class': 'form-control'}))


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'
        exclude = ['user']
        widgets = {
            'nickname': forms.TextInput(attrs={'class': 'form-control'}),
            'avatar': forms.FileInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'phoneNumber': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class CommentForm(forms.ModelForm):

    parent = TreeNodeChoiceField(queryset=Comment.objects.all())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['parent'].widget.attrs.update({'class': 'd-none'})
        self.fields['parent'].required = False

    class Meta:
        model = Comment
        fields = ['parent', 'content', 'author', 'post']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control'}),
            'author': forms.TextInput(attrs={'type': 'hidden'}),
            'post': forms.TextInput(attrs={'type': 'hidden'}),
            'parent': forms.TextInput(attrs={'type': 'hidden'}),
        }
