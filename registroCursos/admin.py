from django.contrib import admin
from .models import UserProfile,Curso,Historial, Asistencia,Encuesta


# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Curso)
admin.site.register(Historial)
admin.site.register(Asistencia)
admin.site.register(Encuesta)
