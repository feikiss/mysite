from django import forms
from mysite import settings

class UserForm(forms.Form):
    username = forms.CharField(label='user name', max_length=100)
    password1 = forms.CharField(label='password', widget=forms.PasswordInput())
    password2 = forms.CharField(label='confirm password', widget=forms.PasswordInput())
    mobile = forms.CharField(label='mobile', widget=forms.NumberInput())

class UserFormLogin(forms.Form):
    username = forms.CharField(label='user name', max_length=100)
    password = forms.CharField(label='password', widget=forms.PasswordInput())

def generate_userid():
    num = settings.SERVER_NUMBER
    return num+''