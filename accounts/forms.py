from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import ModelForm
from accounts.models import Profile

class EditProfileForm(UserChangeForm):
    class Meta:
        model=User
        fields=('username','first_name','last_name','email')

class ProfileForm(UserChangeForm):
    class Meta:
        model=Profile
        fields=('Contact','Address','DOB','Gender')