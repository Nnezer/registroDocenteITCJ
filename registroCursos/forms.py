from django import forms
from .models import Curso,UserProfile
from django.contrib.auth.models import User


class ConfirmForm(forms.Form):
    confirmar = forms.BooleanField(required=True)

class UpdateEmailForm(forms.ModelForm):
 
     class Meta:
        model = User
        fields = ['email',]



class UpdateUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields=['username','password','email','first_name','last_name']



class UpdateUserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields=['sexo','nombramiento','email','grado','departamento','puesto','RFC','CURP']


