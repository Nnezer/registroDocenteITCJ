from django import forms
from .models import Curso,UserProfile
from django.contrib.auth.models import User



class UpdateUsernameForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username',]


class UpdateEmailForm(forms.ModelForm):
        class Meta:
            model = User
            fields = ['email',]
