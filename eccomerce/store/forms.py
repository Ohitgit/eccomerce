from django import forms
from .models import  *
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV3
from django.core.exceptions import ValidationError


class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control form-control_gray'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control form-control_gray'}))

class SignupForm(forms.Form):
    name = forms.CharField(max_length=100, required=True, label="Full Name", widget=forms.TextInput(attrs={'class': 'form-control form-control_gray'}))
    email = forms.EmailField(required=True, label="Email Address", widget=forms.TextInput(attrs={'class': 'form-control form-control_gray'}))
    mobile = forms.CharField(max_length=15, required=True, label="Mobile Number", widget=forms.TextInput(attrs={'class': 'form-control form-control_gray'}))
    password = forms.CharField(
        required=True, label="Password", widget=forms.PasswordInput(attrs={'class': 'form-control form-control_gray'})
    )
    c_password = forms.CharField(
         required=True, label="Confrim Password", widget=forms.PasswordInput(attrs={'class': 'form-control form-control_gray'})
    )
    captcha = ReCaptchaField(
        widget=ReCaptchaV3(action='signup')
    )


    def clean_email(self):
        email = self.cleaned_data.get('email')
       
      
        
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered.")
        return email
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        c_password = cleaned_data.get('c_password')

        if password and c_password and password != c_password:
            raise ValidationError({"c_password": "Passwords do not match."})

        return cleaned_data
    


class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, required=True, label="Full Name", widget=forms.TextInput(attrs={'class': 'form-control form-control_gray'}))
    email = forms.EmailField(required=True, label="Email Address", widget=forms.TextInput(attrs={'class': 'form-control form-control_gray'}))
    mobile = forms.CharField(max_length=15, required=True, label="Mobile Number", widget=forms.TextInput(attrs={'class': 'form-control form-control_gray'}))
    message = forms.CharField(max_length=15, required=True, label="Message", widget=forms.Textarea(attrs={'class': 'form-control form-control_gray'}))
    captcha = ReCaptchaField(widget=ReCaptchaV3(action='signup'))
