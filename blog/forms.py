from django import forms
from django.contrib.auth import get_user_model
from .models import Post, Comment

User = get_user_model()

class Post_form(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'text',)

    def clean_text(self):
        t = self.cleaned_data['text']
        l = []
        for word in t.split(' '):
            if word.lower() in ['жопа', 'porno', 'porn']:
                l.append('cens!')
            else:
                l.append(word)
        return ' '.join(l)

    def clean_title(self):
        t = self.cleaned_data['title']
        l = []
        for word in t.split(' '):
            if word.lower() in ['жопа', 'porno', 'porn']:
                l.append('cens!')
            else:
                l.append(word)
        return ' '.join(l)


class Comment_form(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text', 'page',)

    def clean_text(self):
        t = self.cleaned_data['text']
        l = []
        for word in t.split(' '):
            if word.lower() in ['жопа', 'porno', 'porn']:
                l.append('cens!')
            else:
                l.append(word)
        return ' '.join(l)


class EmailPostForm(forms.Form):
    name = forms.CharField(label='From Name', max_length=25)
    email = forms.EmailField(label='From email')
    to = forms.EmailField(label='Send to email', required=False)
    question = forms.CharField(label='You question' , required=False, widget=forms.Textarea)

    def clean_question(self):
        que = self.cleaned_data['question']
        l = []
        for word in que.split(' '):
            if word.lower() in ['жопа', 'porno', 'porn']:
                l.append('cens!')
            else:
                l.append(word)
        return ' '.join(l)

class RegistrationForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model=User
        fields = ['first_name', 'last_name','password', 'email', 'username']