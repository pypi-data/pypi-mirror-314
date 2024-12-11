from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class customUserCreationform(UserCreationForm):
    class Meta:
       model = User
       fields = ['username', 'password1', 'password2']

    def clean_username(self):
        username = self.cleaned_data['username']

        if not username.isalnum():
            raise forms.ValidationError("El nombre de usuario solo puede contener letras y números.")
        return username