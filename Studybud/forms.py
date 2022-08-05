from django import forms
from .models import User, Room

class LoginForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta():
        model = User
        fields = ['email', 'password']

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta():
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password']

class RoomForm(forms.ModelForm):
    class Meta():
        model = Room
        fields = '__all__'
        exclude = ['participants', 'host']