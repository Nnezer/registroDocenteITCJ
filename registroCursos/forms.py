from django import forms
from .models import *
from django.contrib.auth.models import User

 

class UpdateUserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username','email','first_name','last_name',]


class AddPoll(forms.ModelForm):
    class Meta:
        model: Encuesta

        fields =[]


class UpdateUserProfileForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ['sexo',
        'nombramiento',
        'horas',
        'grado',
        'carrera',
        'area',
        'puesto',
        'telefono_particular',
        'extension',
        'jefe_inmediato',
        'horario_inicio',
        'horario_final',
        'RFC',
        'CURP',]
