from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms 
from .models import Profile

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        
class UserUpdateForm(forms.ModelForm):  # Lets users change username and email.
    class Meta:
        model = User
        fields = ['username', 'email']
        
class ProfileUpdateForm(forms.ModelForm): #Lets users change bio and profile picture.
    class Meta:
         model = Profile
         fields = ['bio', 'profile_picture'] #These forms make sure only allowed fields are updated and also handle form validation automatically.