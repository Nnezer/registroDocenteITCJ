from django.contrib import admin
from .models import UserProfile,Curso,Historial


# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Curso)
admin.site.register(Historial)
