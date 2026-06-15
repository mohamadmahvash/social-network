from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class UserLoginForm(forms.Form):
    username = forms.CharField(label='email/username',
                               widget=forms.TextInput(
                                   attrs={'placeholder': 'Your name', 'class': "form-control"}))

    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': 'Your password', 'class': "form-control"}))


class UserRegisterForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Your name', 'class': "form-control"}))

    email = forms.EmailField(widget=forms.EmailInput(
        attrs={'placeholder': 'Your email', 'class': "form-control"}))

    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': 'Your password', 'class': "form-control"}))

    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': 'confirm password', 'class': "form-control"}))

    def clean_email(self):
        email = self.cleaned_data['email']
        user = User.objects.filter(email=email).exists()
        print(user)
        if user:
            raise ValidationError("this email already exists")
        return email

    def clean_username(self):
        username = self.cleaned_data['username']
        user = User.objects.filter(username=username).exists()
        if user:
            raise ValidationError("this username already exists")
        return username

    def clean(self):
        cd = super().clean()
        p1 = cd.get('password')
        p2 = cd.get('password2')

        if p1 and p2 and p1 != p2:
            raise ValidationError("passwords must match")
