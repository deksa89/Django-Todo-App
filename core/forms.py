from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from .models import Errand

class ErrandForm(forms.ModelForm):
    class Meta:
        model = Errand
        fields = ['title', 'completed']
        

class LoginForm(forms.Form):
    username = forms.CharField(max_length=20)
    password = forms.CharField(max_length=20, widget=forms.PasswordInput)
    

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text='Required. Enter a valid email address.')
    
    class Meta:
        model = User
        fields = ['username', "email", "password1", "password2"]
        
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2:
            if len(password1) < 8:
                raise ValidationError("This password is too short. It must contain at least 8 characters.")
            if password1.isdigit():
                raise ValidationError("This password is entirely numeric.")

        if password1 != password2:
            raise ValidationError("The two password fields didn't match.")

        return password2
        
    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        if commit:
            user.save()
        return user
        