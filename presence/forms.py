# verify/forms.py

from django import forms
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from django.contrib.auth.models import User
from .models import Permission,Service

class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'input mb-3'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input mb-3'}))


class SignUpForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'input mb-3'}))
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={'class': 'input mb-3'}))

    class Meta:
        model = User
        fields = ('username', 'email')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'input mb-3'}),
            'email': forms.EmailInput(attrs={'class': 'input mb-3'}),
        }

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
    
    
from .models import Service  # Assure-toi d'importer ton modèle de service


class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['name']
        
        

from django import forms
from .models import Permission

class PermissionForm(forms.ModelForm):
    start_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'input mb-3', 'required': 'required'}),
        required=True,
        label='Date de début'
    )
    end_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'input mb-3', 'required': 'required'}),
        required=True,
        label='Date de fin'
    )
    reason = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'input mb-3', 'required': 'required'}),
        required=True,
        label='Raison'
    )

    class Meta:
        model = Permission
        fields = ['start_date', 'end_date', 'reason']

            

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']


# forms.p

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['name']