# accounts/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from django.contrib.auth.forms import AuthenticationForm

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone = forms.CharField(required=True)
    year = forms.IntegerField(required=False, min_value=1900, max_value=2100)

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'phone', 'year', 'password1', 'password2')

# accounts/forms.py
class EmailLoginForm(AuthenticationForm):
    username = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={
            'autofocus': True,
            'placeholder': 'Введите ваш email',
            'class': 'input-field w-full px-4 py-3 rounded-xl bg-white bg-opacity-70 text-gray-800 placeholder-gray-500 font-medium'
        })
    )
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Введите ваш пароль',
            'class': 'input-field w-full px-4 py-3 rounded-xl bg-white bg-opacity-70 text-gray-800 placeholder-gray-500 font-medium'
        })
    )

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username:
            username = username.lower()
        return username

from django import forms
from .models import Course

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'subject', 'tags', 'level', 'description']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Название курса'}),
            'subject': forms.Select(attrs={'class': 'form-control'}),
            'tags': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Например: математика, наука, вычисления'}),
            'level': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Описание курса'}),
        }

class CourseStructureForm(forms.Form):
    topics = forms.CharField(widget=forms.HiddenInput(), required=False)
    lessons = forms.CharField(widget=forms.HiddenInput(), required=False)

