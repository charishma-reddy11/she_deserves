from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(required=True)
    address = forms.CharField(widget=forms.Textarea, required=False) # Optional chesam
    
    class Meta:
        model = CustomUser
        # 'username' ni theesesi 'email' pettandi, endukante mana model lo username ledu
        fields = ('email', 'first_name', 'last_name', 'phone_number', 'address')

class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'phone_number', 'address')
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
        }