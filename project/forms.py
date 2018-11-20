from django import forms
from django.forms import ModelForm

from project.models import User


class RegistrationForm(forms.Form):
    name = forms.CharField(label='First Name', max_length=100)
    last_name = forms.CharField(label='Last Name', max_length=100)
    username = forms.CharField(label='Username', max_length=100)
    password = forms.CharField(label='Password', max_length=50, widget=forms.PasswordInput)
    token = forms.CharField(label='Token', max_length=1000)

class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100)
    password = forms.CharField(label='Password', max_length=50, widget=forms.PasswordInput)

class TokenForm(forms.Form):
    email = forms.EmailField(label='Email', max_length=100)
    role = forms.CharField(label='Role',max_length=2)
