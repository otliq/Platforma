from django import forms
from django.contrib.auth.forms import AuthenticationForm

class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Username', 
                               widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Password', 
                               widget=forms.PasswordInput(attrs={'class': 'form-input'}))