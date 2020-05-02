from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm,AuthenticationForm
from django.forms import ModelForm
from accounts.models import Profile
from django.conf import settings
from django.core.mail import send_mail

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

class OTPAuthenticationForm(AuthenticationForm):
    otp = forms.CharField(required=False, widget=forms.PasswordInput)

    def clean(self):
        # Allow Django to detect can user log in
        super(OTPAuthenticationForm, self).clean()

        # If we got this far, we know that user can log in.
        if self.request.session.has_key('_otp'):
            if self.request.session['_otp'] != self.cleaned_data['otp']:
                raise forms.ValidationError("Invalid OTP.")
            del self.request.session['_otp']
        else:
            # There is no OTP so create one and send it by email
            otp = "1234"
            send_mail(
                subject="Your OTP Password",
                message="Your OTP password is %s" % otp,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[self.user_cache.email]
            )
            self.request.session['_otp'] = otp
            # Now we trick form to be invalid
            raise forms.ValidationError("Enter OTP you received via e-mail")