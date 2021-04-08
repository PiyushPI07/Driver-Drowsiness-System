from django import forms
from django.contrib.auth.forms import UserCreationForm 
from django.contrib.auth import authenticate
from .models import *

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=60)
    class Meta:
        model = Account
        fields = ('dl_number', 'driver_name', 'email', 'phone_number', 'emergency_phn')
class SettingsForm(forms.ModelForm):
    # email = forms.EmailField(max_length=60, widget = forms.TextInput(attrs={'readonly':'readonly'}))
    # dl_number = forms.EmailField(max_length=60, widget = forms.TextInput(attrs={'readonly':'readonly'}))
    # driver_name = forms.EmailField(max_length=60, widget = forms.TextInput(attrs={'readonly':'readonly'}))
    class Meta:
        model = Account
        fields = ('dl_number', 'driver_name', 'email', 'phone_number', 'emergency_phn')
class ChangeAlertForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ('alert_tone',)
class LoginForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    class Meta:
        model = Account
        fields = ('email', 'password')
    def clean(self):
        # email = self.cleaned_data['email'].lower()
        email = MyAccountManager.normalize_email(self.cleaned_data['email'])
        password = self.cleaned_data['password']
        if not authenticate(email = email, password = password):
            raise forms.ValidationError('Invalid Credentials')