from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import ModelForm
from accounts.models import Profile

class EditProfileForm(UserChangeForm):
    username= forms.CharField(label='username',max_length=50,required=True,widget=forms.TextInput(attrs={'class':'form-control','name':'username'}))
    first_name= forms.CharField(label='first_name',max_length=50,required=True,widget=forms.TextInput(attrs={'class':'form-control','name':'first_name'}))
    last_name= forms.CharField(label='last_name',max_length=50,required=True,widget=forms.TextInput(attrs={'class':'form-control','name':'last_name'}))
    email= forms.CharField(label='email',max_length=50,required=True,widget=forms.TextInput(attrs={'class':'form-control','name':'email'}))
    #password= forms.CharField(label='password',max_length=50,required=True,widget=forms.PasswordInput(attrs={'class':'form-control','name':'password'}))
    class Meta:
        model=User
        fields=('username','first_name','last_name','email','password')

class ProfileForm(UserChangeForm):
    Contact= forms.CharField(label='Contact',max_length=20,required=True,widget=forms.TextInput(attrs={'class':'form-control','name':'Contact'}))
    Address= forms.CharField(label='Address',max_length=50,required=True,widget=forms.TextInput(attrs={'class':'form-control','name':'Address'}))
    DOB= forms.DateField(label='DOB',required=True,widget=forms.DateInput(attrs={'class':'form-control','name':'DOB'}))
    Gender= forms.CharField(label='Gender',max_length=10,required=True,widget=forms.TextInput(attrs={'class':'form-control','name':'Gender'}))
    class Meta:
        model=Profile
        fields=('Contact','Address','DOB','Gender')