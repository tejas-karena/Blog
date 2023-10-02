from django import forms
from .models import Comment, Post, User
from django.contrib.auth.forms import UserCreationForm


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["username", "commentblog", "comment"] 
        exclude = ["commentblog"]

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            "email",
            "first_name",
            "last_name",
            "country",
            "birth_date",
            "password1",
            "password2"
        ]
        labels = {
            "email": "Email",
            "first_name": "First Name",
            "last_name": "Last Name",
            "country": "Country",
            "birth_date": "Birthdate",
            "password1":"Password",
            "Password2":"Password confirmation" 
        }
        widgets = {
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "country": forms.TextInput(attrs={"class": "form-control"}),
            "birth_date": forms.DateInput(attrs={"class": "form-control","type":"Date"}),
            "password1": forms.PasswordInput(attrs={"class": "form-control"}),
            "password2": forms.PasswordInput(attrs={"class": "form-control"}),
        }


class BlogAddForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'blog']

class SearchForm(forms.Form):
    search = forms.CharField(label='Search', max_length=100, required=False)

