from django import forms
from django.contrib.auth.models import User
from .models import student

class StudentRegistrationForm(forms.ModelForm):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = student
        fields = ['full_name', 'course', 'academic_year', 'photo', 'town']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match")
        

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


# forms.py (add below your existing code)
class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username']  # include 'username' if you want

class StudentUpdateForm(forms.ModelForm):
    class Meta:
        model = student
        fields = ['full_name', 'course', 'academic_year', 'photo', 'town']
