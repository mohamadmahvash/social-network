from django import forms


class UserRegisterForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Your name', 'class': "form-control"}))

    email = forms.EmailField(widget=forms.EmailInput(
        attrs={'placeholder': 'Your email', 'class': "form-control"}))

    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': 'Your password', 'class': "form-control"}))
