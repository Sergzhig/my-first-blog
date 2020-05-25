from django import forms

from .models import Post, Comment


class Post_form(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'text',)


class Comment_form(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text', 'page',)
