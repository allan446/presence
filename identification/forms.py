# verify/forms.py

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from .models import Permission

class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class PermissionForm(forms.ModelForm):
    class Meta:
        model = Permission
        fields = ['reason']
        widgets = {
            'reason': forms.Textarea(attrs={'class': 'form-control'}),
        }

