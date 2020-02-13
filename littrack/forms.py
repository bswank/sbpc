from django import forms
from django.forms import ValidationError
from django.contrib.auth.models import User

class RegisterForm(forms.Form):
    first = forms.CharField(max_length=50, label='First Name')
    last = forms.CharField(max_length=50, label='Last Name')
    email = forms.EmailField(label='Email Address')
    password = forms.CharField(widget=forms.PasswordInput, min_length=1)

    def clean_email(self):
        email = self.cleaned_data['email']

        if User.objects.filter(email=email).exists():
            print('hello')
            raise ValidationError('Oops! A user with that email address already exists! Try signing in instead.')

        return email

class SearchBookForm(forms.Form):
    search_term = forms.CharField(max_length=200, label='Book Title')

class AddBookForm(forms.Form):
    title = forms.CharField(max_length=50)
    author = forms.CharField(max_length=50)
    rating = forms.NumberInput()

class EditBookForm(forms.Form):
    title = forms.CharField(max_length=300)
    authors = forms.CharField(max_length=400)
    isbn13 = forms.CharField(max_length=13, label='ISBN13')
    cover = forms.CharField(max_length=300, label='Cover Image URL')
    rating = forms.IntegerField(min_value=1, max_value=5, label='Rating (1-5)', required=False)
