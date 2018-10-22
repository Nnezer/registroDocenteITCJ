from django import forms
from .models import Curso,UserProfile
from django.contrib.auth.models import User

class UpdateUserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username','email','first_name','last_name',]


class UpdateUserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['sexo','nombramiento','grado','departamento','puesto','telefono_particular', 'RFC','CURP',]