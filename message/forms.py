
from django import forms
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile,Contactus

class RegistrationForm(UserCreationForm):
    first_name=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
        
    last_name=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
        
    
    username=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
        
    email = forms.CharField(widget=forms.EmailInput(attrs={'class':'form-control'}))
    password1 = forms.CharField(label='password', widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(label='Repeat_password', widget=forms.PasswordInput(attrs={'class':'form-control'}))
        
    
    

    class Meta:
        model = User
        
        fields = ('first_name','last_name','username','email', 'password1', 'password2')

    # def save(self, commit=False):
    #     user = super(RegistrationForm, self).save(commit=False)
       
    #     user.first_name=self.cleaned_data['first_name']
    #     user.last_name=self.cleaned_data['last_name']
    #     user.username=self.cleaned_data['username']
    #     user.email = self.cleaned_data['email']
        
    #     if commit:
    #         user.save()
    #     return user
class UserLoginForm(AuthenticationForm):
    username=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control',}))
    # email = forms.CharField(widget=forms.EmailInput(attrs={'class':'form-control',
    #                                                         'placeholder':'email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                 'placeholder': 'password',
                                                                 'id': 'login-pwd'}))
class ContactForm(forms.ModelForm):
    class Meta:
        model=Contactus
        fields=['name','email','subject','message']
    message = forms.CharField(widget=forms.Textarea)


