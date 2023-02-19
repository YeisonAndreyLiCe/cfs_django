from django import forms
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _
from users.models import User
import re


class RegisterForm(ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control mb-3'}))
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password']
        help_texts = {
            'password': _(
                '''Password must be at least 8 characters<br>
                contain at least one number<br>
                one uppercase and one lowercase letter.'''
                ),
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control mb-3'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control mb-3'}),
            'email': forms.EmailInput(attrs={'class': 'form-control mb-3'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control mb-3'}),
            'help_text': forms.TextInput(attrs={'class': 'form-text mb-3'}),
        }

    def clean_password(self):
        re_password = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$')
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        if not re_password.match(password):
            raise forms.ValidationError("Password must be at least 8 characters, contain at least one number, one uppercase and one lowercase letter")
        return password
    
    def clean_email(self):
        cleaned_data = super().clean()
        re_email = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        email = cleaned_data.get('email')
        if not re_email.match(email):
            raise forms.ValidationError("Invalid email address")
        return email