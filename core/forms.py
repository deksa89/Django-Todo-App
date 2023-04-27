from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Errand

class ErrandForm(forms.ModelForm):
    class Meta:
        model = Errand
        fields = ['title', 'completed']
        

class LoginForm(forms.Form):
    username = forms.CharField(max_length=20)
    password = forms.CharField(max_length=20, widget=forms.PasswordInput)
    

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', "password1", "password2"]
        
    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        if commit:
            user.save()
        return user
        